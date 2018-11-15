from datetime import datetime

def is_datetime(datetime_string):
  # Check the arg is able to be converted to datetime object
  try:
    datetime.strptime(datetime_string, '%Y-%m-%d %H:%M:%S')
    return True
  except:
    return False
