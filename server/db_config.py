from peewee import SqliteDatabase


# In-memory databases are allowed to use shared cache if they are opened using
# a URI filename. If the unadorned ":memory:" name is used to specify the in-memory
# database, then that database always has a private cache and is only visible
# to the database connection that originally opened it. However, the same in-memory
# database can be opened by two or more database connections as follows:
# refer: https://www.sqlite.org/inmemorydb.html#sharedmemdb
db = SqliteDatabase('file::memory:?cache=shared')
# db = SqliteDatabase('test.db')
