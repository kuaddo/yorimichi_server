from models.users import create_user, get_posts_by_uuid, add_point, get_user_by_uuid
from models.point_history import create_point_history
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
  # API Token exist?
  if 'X_API_Token' not in request.headers:
    return make_response(jsonify({'message': 'API token not found'}), 400)
  # API Token Correct?
  if not check_api_token(request.headers['X_API_Token']):
    return make_response(jsonify({'message': 'API token is not correct'}), 400)
  res = get_posts_by_uuid(uuid)
  
  if len(res) > 0:
    return make_response(jsonify({'message': 'Request Completed.', 'posts_array': res}), 200)
  else:
    return '', 204

@app.route('<uuid>/points/', methods=['POST'])
def points(uuid):
  # API Token exist?
  if 'X_API_Token' not in request.headers:
    return make_response(jsonify({'message': 'API token not found'}), 400)
  # API Token Correct?
  if not check_api_token(request.headers['X_API_Token']):
    return make_response(jsonify({'message': 'API token is not correct'}), 400)

  # check Content-Type header
  if 'application/json' not in  request.headers['Content-Type'].split(';'):
    return make_response(jsonify({'message': 'error'}), 400)

  # check request json contains item 'point'?
  if 'point' not in request.json:
    return make_response(jsonify({'message': 'Require point'}), 400)
  
  user_records = get_user_by_uuid(uuid)
  if len(user_records) == 0:
    return make_response(jsonify({'message': 'No user found on specified uuid'}), 400)

  add_point(uuid, request.json['point'])
  create_point_history(user_records[0]['id'], request.json['point'])

  return make_response(jsonify({'message': 'Points successfuly gave to user.'}), 200)