from models.connector import query

def visit(user_id, place_uid):
  now = datetime.now()
  now_str = now.strftime('%Y-%m-%d %H:%M:%S')
  stmt = """
    INSERT INTO visit_histry
    (place_uid, user_id, created_at, updated_at, is_valid)
    VALUES ("{}", {}, "{}", "{}", 1)
  """.format(place_uid, user_id, now_str, now_str)

  query(stmt)

  return