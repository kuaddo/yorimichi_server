from models.connector import query

from datetime import datetime

def create(image_name, user_id, place_uid):
  now_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
  stmt = """
    INSERT INTO posts (user_id, image_name, place_uid, created_at, updated_at, is_valid)
    VALUES ({}, "{}", "{}", "{}", "{}", 1)
  """.format(str(user_id), image_name, place_uid, now_str, now_str)
  query(stmt)

  return