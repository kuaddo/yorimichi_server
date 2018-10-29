from models.connector import query

from datetime import datetime

def create_point_history(user_id, points):
  now = datetime.now()
  now_str = now.strftime('%Y-%m-%d %H:%M:%S')

  stmt = '''
    INSERT INTO points_history (user_id, points, created_at, updated_at, is_valid)
    VALUES ({}, {}, \"{}\", \"{}\", 1)
  '''.format(user_id, points, now_str, now_str)

  query(stmt)
  return