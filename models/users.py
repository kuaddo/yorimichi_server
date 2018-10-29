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

def get_user_by_uuid(uuid):
  stmt = 'SELECT * FROM users WHERE uuid = \'{}\''.format(uuid)
  return query(stmt)

def get_posts_by_uuid(uuid):
  stmt = '''
    SELECT  p.id AS id,
            p.user_id AS user_id,
            p.place_uid AS place_uid,
            "gs://yorimichi_posts" AS bucket,
            p.image_name AS image_name,
            DATE_FORMAT(p.created_at, '%Y-%m-%d %H:%i:%S') AS created_at,
            DATE_FORMAT(p.updated_at, '%Y-%m-%d %H:%i:%S') AS updated_at
    FROM    posts AS p
      INNER JOIN users AS u ON u.id = p.user_id
    WHERE   u.uuid = "{}"
      AND   u.is_valid = 1
      AND   p.is_valid = 1
  '''.format(uuid)

  res = query(stmt)
  return res

def add_point(uuid, point):
  stmt = '''
    UPDATE  users
    SET     points = points + {}
    WHERE   uuid = \"{}\"
  '''.format(point, uuid)

  query(stmt)

  return