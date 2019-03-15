# ALBot SQL Backend

This directory contains files for ALBot's SQLite3 database backend.

## Using the SQL backend

The following examples show how to use the SQL backend:

**Basic usage:**
```python
from sql.sql import SQLConnection, SQLCursor, SQLRollback

connection = SQLConnection() # Checks the database integrity and returns a new connection object
with SQLCursor(connection) as cursor: # The backend uses a context manager to wrap the cursor object
	""" Get data from some_table """
	cursor.execute('SELECT * FROM some_table;')
	result = cursor.fetchall()

# 'result' now contains all returned rows.
```

**Sanitizing input values:**
```python
some_message_id = 484572171608522771
some_message_text = 'The Spanish Inquisition'
with SQLCursor(connection) as cursor:
	""" Insert values into some_table, sanitizing them to prevent naughty business. """
	cursor.execute('INSERT INTO some_table (message_id, message_text) VALUES (?,?);', (some_message_id, some_message_text))

print('done') # Changes are automatically committed at the end of the 'with' statement.
```

**Rolling back changes:**
```python
some_message_id = 484554017884602380
some_message_text = 'My most embarassing secrets that I would never want in an SQLite database'
message_is_regretted = True

with SQLCursor(connection) as cursor:
	""" Insert a value, then roll it back """
	cursor.execute('INSERT INTO some_table (message_id, message_text) VALUES (?, ?);', (some_message_id, some_message_text))

	if message_is_regretted:
		raise SQLRollback() # This is a special exception type which is handled by the context manager. When it is raised, the context manager will rollback the pending database changes and jump to the end of the 'with' statement.
	
	print('Message was not regretted') # The program will not reach this line if SQLRollback is raised.

print('done') # The changes are rolled back, and your embarassing secrets are safe.
```

For more information, see the [SQLite3 library documentation](https://docs.python.org/3.6/library/sqlite3.html) (note that the SQLite3 Connection object is not the same as the backend's SQLConnection object; however, the SQLite3 library Connection object can be retrieved using the `raw` attribute of an SQLConnection object).

## Adding new tables

The backend uses the file `data/schema.json` to determine how the database should be structured. By modifying this file, the table structure can be modified. Note, however, that changes to the structure of existing tables will cause the backend to detect the database as corrupt (this does not happen when new tables are added - the backend will simply create the new tables to match the schema).
