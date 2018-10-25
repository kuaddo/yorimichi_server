import os
import secrets

def check_api_token(token):
  return secrets.compare_digest(token, os.environ['API_KEY'])