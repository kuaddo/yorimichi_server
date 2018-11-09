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
      
      stmt = 'SELECT * FROM users WHERE uuid = \"{}\"'.format(uuid)
      user = query(stmt)[0]

      # make default users_goods records
      stmt = '''
        INSERT INTO users_goods 
          (user_id, goods_id, created_at, updated_at, is_valid)
        SELECT	users.id, t.id, NOW(), NOW(), 1
        FROM	users, 
              (SELECT id FROM goods WHERE id in (1, 2, 11, 12, 21)) AS t
        WHERE users.id = {}
      '''.format(user['id'])
      query(stmt)

      return user

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
  now = datetime.now()
  now_str = now.strftime('%Y-%m-%d %H:%M:%S')

  stmt = '''
    UPDATE  users
    SET     points = points + {},
            updated_at = \"{}\"
    WHERE   uuid = \"{}\"
  '''.format(point, now_str, uuid)

  query(stmt)

  return

def purchase_goods(user_id, goods_id):
  check_user_goods_query = '''
    SELECT  *
    FROM    users_goods
    WHERE   user_id = {}
      AND   goods_id = {}
  '''.format(user_id, goods_id)

  if len(query(check_user_goods_query)) > 0:
    return {'message': 'User already have this goods'}, 400

  user_points_query = '''
    SELECT  *
    FROM    users
    WHERE   id = {}
  '''.format(user_id)

  user_points = query(user_points_query)[0]['points']

  require_points_query = '''
    SELECT  *
    FROM    goods
    WHERE   id = {}
  '''.format(goods_id)

  ret = query(require_points_query)
  if len(ret) == 0:
    return {'message': 'Specified goods not found.'}, 400

  require_points = ret[0]['value']

  if user_points < require_points:
    # User don't have enough points
    return {'message': 'User do not have enough points to parchase.'}, 400
  
  user_update_query = '''
    UPDATE  users
    SET     points = points - {}
    WHERE   id = {}
  '''.format(require_points, user_id)

  user_goods_insert_query = '''
    INSERT INTO users_goods (user_id, goods_id, created_at, updated_at, is_valid)
    VALUES ({}, {}, NOW(), NOW(), 1)
  '''.format(user_id, goods_id)

  query(user_update_query)
  query(user_goods_insert_query)

  return {}, 200