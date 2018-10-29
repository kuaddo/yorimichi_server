from models.users import create_user, get_posts_by_uuid
from utils.token import check_api_token

from flask import Blueprint, jsonify, make_response, request

app = Blueprint('users', __name__, url_prefix='/v1/users')

@app.route('/', methods=['GET', 'POST'])
def index():
  # API Token exist?
  if 'X_API_Token' not in request.headers:
    return make_response(jsonify({'message': 'API token not found'}), 400)
  # API Token Correct?
  if not check_api_token(request.headers['X_API_Token']):
    return make_response(jsonify({'message': 'API token is not correct'}), 400)
  # API Key Corrected, begin create user.
  if request.method == 'POST':
    uuid = create_user()
    return make_response(jsonify({'message': 'Create User.', 'uuid': uuid}))
  else:
    return make_response(jsonify({'message': 'This is user view root'}))

@app.route('/<uuid>/posts/', methods=['GET'])
def posts(uuid):
  res = get_posts_by_uuid(uuid)
  
  if len(res) > 0:
    return make_response(jsonify({'message': 'Request Completed.', 'posts_array': res}), 200)
  else:
    return '', 204