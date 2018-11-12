from models.connector import query

def visit(user_id, place_uid):
  stmt = """
    INSERT INTO visit_history
    (place_uid, user_id, created_at, updated_at, is_valid)
    VALUES ("{}", {}, NOW(), NOW(), 1)
  """.format(place_uid, user_id)

  query(stmt)

  return