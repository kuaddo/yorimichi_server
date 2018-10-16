from models.connector import query

from uuid import uuid4
from datetime import datetime

def create_user():
  # create 
  for i in range(5):
    uuid = str(uuid4())

    stmt = 'SELECT * FROM users WHERE uuid = \"{}\"'.format(uuid)
    ret = query(stmt)

    if len(ret) == 0:
      now = datetime.now()
      now_str = now.strftime('%Y-%m-%d %H:%M:%S')
      stmt = '''
        INSERT INTO users (uuid, points, created_at, updated_at, is_valid)
        VALUES (\"{}\", 0, \"{}\", \"{}\", 1)
      '''.format(uuid, now_str, now_str)
      query(stmt)
      return uuid

  return None

def get_user(uuid):
  stmt = 'SELECT * FROM users WHERE uuid = \'{}\''.format(uuid)
  return query(stmt)