class SQLConnection():
	''' Abstract class for an SQL database type '''
	def __init__(self):
		self._TYPE = 'Abstract base class'
	
	def get_pydal_string(self):
		pass
	
	def __str__(self):
		return '{ctype} database connection type with string {pstr}'.format(ctype=self._TYPE, pstr=self.get_printing_pydal_string())

class SQLITE3_CONNECTION(SQLConnection):
	def __init__(self, database_file_location):
		self._TYPE = 'SQLite3'
		self.db_file = database_file_location
	
	def get_pydal_string(self):
		return 'sqlite://{0}'.format(self.db_file)

	def get_printing_pydal_string(self):
		return 'sqlite://{0}'.format(self.db_file)
	
class POSTGRESQL_CONNECTION(SQLConnection):
	def __init__(self, db_username, db_password, db_name, db_url='127.0.0.1', db_port=5432):
		self._TYPE = 'PostgreSQL'
		self.db_username = db_username
		self.db_password = db_password
		self.db_name = db_name
		self.db_url = db_url
		self.db_port = db_port
	
	def get_pydal_string(self):
		return 'postgres://{user}:{pasw}@{url}:{port}/{name}'.format(\
			user=self.db_username,\
			pasw=self.db_password,\
			url=self.db_url,\
			port=self.db_port,\
			name=self.db_name)

	def get_printing_pydal_string(self):
		return 'mysql://{user}:[password]@{url}:{port}/{name}'.format(\
			user=self.db_username,\
			url=self.db_url,\
			port=self.db_port,\
			name=self.db_name)
	
class MYSQL_CONNECTION(SQLConnection):
	def __init__(self, db_username, db_password, db_name, db_url='127.0.0.1', db_port=5432):
		self._TYPE = 'MySQL'
		self.db_username = db_username
		self.db_password = db_password
		self.db_name = db_name
		self.db_url = db_url
		self.db_port = db_port
	
	def get_pydal_string(self):
		return 'mysql://{user}:{pasw}@{url}:{port}/{name}'.format(\
			user=self.db_username,\
			pasw=self.db_password,\
			url=self.db_url,\
			port=self.db_port,\
			name=self.db_name)

	def get_printing_pydal_string(self):
		return 'mysql://{user}:[password]@{url}:{port}/{name}'.format(\
			user=self.db_username,\
			url=self.db_url,\
			port=self.db_port,\
			name=self.db_name)
