import sqlite3
import json

class DatabaseInitializeError(BaseException):
	'''
	  ' Raised when the database can't be initialized properly
	'''

class SQLRollback(BaseException):
	'''
	  ' Raise this exception to rollback an SQLCursor operation
	'''

class SQLCursor:
	'''
	  ' Cursor object for sqlite3 database.
		' Manages automatic creation/committing of data.
		' 
		' To use:
		' 	connection = SQLConnection()
		'   
		'   with SQLCursor(connection) as cursor:
		'     do_things_with(cursor)
		' 		if something_is_wrong:
		'       raise SQLRollback() # Raise this exception to jump out of the
		'                             with statement and rollback the changes

		'   do_other_things() # Cursor object is closed and committed before
		'                       this line, unless SQLRollback was raised
	'''
	def __init__(self, connection):
		''' Initialize database connection '''
		self.con = connection
	
	def __enter__(self):
		''' Create and return cursor '''
		self.cur = self.con.raw.cursor()
		return self.cur
	
	def __exit__(self, xtype, xvalue, xtraceback):
		''' If SQLRollback was raised, rollback changes and exit 
		  ' Otherwise, commit and exit.
		'''
		if xtype == SQLRollback:
			self.con.raw.rollback()
		else:
			self.con.raw.commit()

		self.cur.close()

		return xtype == SQLRollback # If the exception was SQLRollback, suppress
		                            # normal exception handling.

class SQLConnection:
	def __init__(self):
		''' Check database integrity, create missing tables, and prompt the user
		  ' to re-initialize if table schema does not match expected values.
		'''
		self.table_prefix = ''
		self.raw = sqlite3.connect('data/sqlite3.db')
		with open('sql/schema.json') as schema_file:
			self.schema = json.load(schema_file)

		table_status = self.table_check()
		if table_status == 0:
			return
		elif table_status == 1:
			print('[database] Database is empty. Initializing...')
			self.setup_tables(force=False)
		elif table_status == 2:
			print('[database] Some tables are missing. Creating missing tables...')
			self.setup_tables(force=False)
		else:
			print('[database] SEVERE: Database does not match expected schema! Re-initialize?')
			reinit = input('[y/n]:')
			if reinit.lower() == 'y':
				print('[database] WARNING: Deleting all data and re-initializing...')
				self.setup_tables(force=True)
			else:
				print('[database] FATAL: Table setup cannot continue. Aborting.')
				raise DatabaseInitializeError('FATAL: Table setup aborted by user.')
	
	def table_check(self, schema=None, table_prefix=None):
		'''
		  ' Verify the table structure in the database
			' 
			' Parameters:
			'   schema = dict from schema.json, detailing the expected
			'            table schema for the database.
			' 
			'   table_prefix = if present, prepend this to table names as
			'                  specified in the schema.
			' 
			' Returns:
			'   0 if everything is normal
			'   1 if the database is empty
			'   2 if some tables are present but others are absent
			'   3 if tables do not follow the expected schema
		'''
		if not schema:
			schema = self.schema
		if not table_prefix:
			table_prefix = self.table_prefix
			
		all_tables_present = True
		database_empty = True
		schema_ok = True

		with SQLCursor(self) as cur:
			cur.execute("SELECT name FROM sqlite_master WHERE type = 'table';")
			res_raw = cur.fetchall()

		res_fixed = []
		for result in res_raw:
			res_fixed.append(result[0])

		for table in schema:
			tname = table_prefix + table['name']
			if tname in res_fixed:
				database_empty = False
				with SQLCursor(self) as cur:
					cur.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='{0}'".format(tname))
					res_raw = cur.fetchall()
					res_preproc = res_raw[0][0][res_raw[0][0].find('(')+1:res_raw[0][0].find(')')].split(',')
					res = []
					for column in res_preproc:
						column = column.strip()
						column_processed = [column[:column.find(' ')], column[column.find(' ')+1:].split(' ')[0]]
						res.append(column_processed)
				
				if len(res) != len(table['schema']):
					print('[database] SEVERE: missing column(s)')
					schema_ok = False # missing column(s)

				for column in res:
					match = False
					for col_descriptor in table['schema']:
						if col_descriptor['name'] == column[0]:
							if col_descriptor['type'].lower() == column[1].lower():
								match = True
								break
							else:
								print('[database] SEVERE: type mismatch on column {0}'.format(column))
								schema_ok = False # Type mismatch

					if not match:
						print('[database] SEVERE: unexpected column {0}'.format(column))
						schema_ok = False # Unexpected column

			else:
				all_tables_present = False # missing table

		if not schema_ok:
			return 3
		elif database_empty:
			return 1
		elif not all_tables_present:
			return 2
		else:
			return 0

	def setup_tables(self, force=False):
		'''
		  ' Sets up the proper tables in the sqlite3 database
			' 
			' Parameters:
			'   force = whether to delete all tables and re-initialize. This
			'           option is DANGEROUS, and should not be used unless
			'           necessary
		'''

		if force: # delete all present tables
			with SQLCursor(self) as cur:
				cur.execute("SELECT name FROM sqlite_master WHERE type = 'table';")
				table_list_unfixed = cur.fetchall()

				for table in table_list_unfixed:
					tname = table[0]
					cmd = 'DROP TABLE ' + tname + ';'
					print('[database] Removing table {0}.'.format(tname))
					cur.execute(cmd)

		with SQLCursor(self) as cur:
			cur.execute("SELECT name FROM sqlite_master WHERE type = 'table';")
			table_list_unfixed = cur.fetchall()

			table_list = []

			for table in table_list_unfixed:
				table_list.append(table[0])

			for table in self.schema:
				tname = self.table_prefix + table['name']
				if tname in table_list:
					continue # ignore tables which already exist
				else:
					cmd = 'CREATE TABLE ' + tname + ' ('
					for index, column in enumerate(table['schema']):
						if index != 0:
							cmd = cmd + ', '
						cmd = cmd + column['name'] + ' ' + column['type']
						if 'primary' in column: # columns with primary:true are PRIMARY KEY columns
							if column['primary']:
								cmd = cmd + ' PRIMARY KEY'
					
					cmd = cmd + ');'
					print('[database] Creating table {0} with command `{1}`.'.format(tname, cmd))
					cur.execute(cmd) # create table
