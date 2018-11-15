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

def get_posts_by_place(place_uid, time=None):
  if time is None:
    time = "NOW()"
  else:
    time = '\"' + time + '\"'

  stmt = """
    SELECT  p.id AS id,
            p.user_id AS user_id,
            p.place_uid AS place_uid,
            "gs://yorimichi_posts" AS bucket,
            p.image_name AS image_name,
            p.created_at,
            p.updated_at
    FROM    posts AS p
    WHERE   p.is_valid = 1
      AND   p.place_uid = "{}"
      AND   p.created_at <= {}
    ORDER BY created_at DESC
  """.format(place_uid, time)

  res = query(stmt)
  return res