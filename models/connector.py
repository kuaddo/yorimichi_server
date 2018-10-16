from models.config import config

import pymysql

def query(statement):
  conn = pymysql.connect(**config)
  cursor = conn.cursor()

  cursor.execute(statement)
  res = cursor.fetchall()
  cursor.close()
  conn.close()

  return res