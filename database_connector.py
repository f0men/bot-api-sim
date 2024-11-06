import psycopg2
from psycopg2.extras import RealDictCursor
class DataBase:

  def __new__(cls, *args, **kwargs):
    if not hasattr(cls, 'instance'):
      cls.instance = super(DataBase, cls).__new__(cls)
    return cls.instance
  def __init__(self, host, port, database, user, password, autocommit=False):
    self.connection = psycopg2.connect(
        host = host,
        port = port,
        database = database,
        user = user,
        password = password
    )
    self.cursor = self.connection.cursor(cursor_factory=RealDictCursor)
    if autocommit:
      self.connection.autocommit = True

  def select(self, query):
    self.cursor.execute(query)
    if not self.connection.autocommit:
      self.connection.commit()
    return self.cursor.fetchall()
  
  def insert(self, query):
    self.cursor.execute(query)
    self.connection.commit()

  def return_all_tables(self):
    self.cursor.execute('''select table_name from information_schema.tables where table_schema not in ('information_schema','pg_catalog')''')
    return self.cursor.fetchall()