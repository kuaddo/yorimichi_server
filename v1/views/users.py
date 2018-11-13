from models.users import create_user, get_posts_by_uuid, add_point, get_user_by_uuid, purchase_goods, change_icon
from models.point_history import create_point_history
from models.goods import get_goods
from models.visit_history import visit, visit_history
from utils.apitoken import check_api_token

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
    created_user = create_user()
    return make_response(jsonify(created_user))
  else:
    return make_response(jsonify({'message': 'This is user view root'}))

@app.route('/<uuid>/', methods=['GET'])
def get_user(uuid):
  # API Token exist?
  if 'X_API_Token' not in request.headers:
    return make_response(jsonify({'message': 'API token not found'}), 400)
  # API Token Correct?
  if not check_api_token(request.headers['X_API_Token']):
    return make_response(jsonify({'message': 'API token is not correct'}), 400)

  res = get_user_by_uuid(uuid)

  if len(res) > 0:
    return make_response(jsonify(res[0]), 200)
  else:
    return '', 204

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

  res = get_user_by_uuid(uuid)

  return make_response(jsonify(res[0]), 200)

@app.route('<uuid>/goods/', methods=['GET'])
def goods(uuid):
  # API Token exist?
  if 'X_API_Token' not in request.headers:
    return make_response(jsonify({'message': 'API token not found'}), 400)
  # API Token Correct?
  if not check_api_token(request.headers['X_API_Token']):
    return make_response(jsonify({'message': 'API token is not correct'}), 400)

  user_records = get_user_by_uuid(uuid)
  if len(user_records) == 0:
    return make_response(jsonify({'message': 'No user found on specified uuid'}), 400)

  ret = get_goods(user_records[0]['id'])
  return make_response(jsonify(ret), 200)

@app.route('<uuid>/purchase/goods/<goods_id>/', methods=['POST'])
def purchase(uuid, goods_id):
  # API Token exist?
  if 'X_API_Token' not in request.headers:
    return make_response(jsonify({'message': 'API token not found'}), 400)
  # API Token Correct?
  if not check_api_token(request.headers['X_API_Token']):
    return make_response(jsonify({'message': 'API token is not correct'}), 400)

  user_records = get_user_by_uuid(uuid)
  if len(user_records) == 0:
    return make_response(jsonify({'message': 'No user found on specified uuid'}), 400)

  content, code = purchase_goods(user_records[0]['id'], goods_id)

  if code == 400:
    return make_response(jsonify(content), code)

  ret = get_goods(user_records[0]['id'])
  return make_response(jsonify(ret), 200)

@app.route('<uuid>/icon/<icon_id>/', methods=['PATCH'])
def set_icon(uuid, icon_id):
  # API Token exist?
  if 'X_API_Token' not in request.headers:
    return make_response(jsonify({'message': 'API token not found'}), 400)
  # API Token Correct?
  if not check_api_token(request.headers['X_API_Token']):
    return make_response(jsonify({'message': 'API token is not correct'}), 400)

  user_records = get_user_by_uuid(uuid)
  if len(user_records) == 0:
    return make_response(jsonify({'message': 'No user found on specified uuid'}), 400)

  content, code = change_icon(user_records[0]['id'], icon_id)

  if code == 400:
    return make_response(jsonify(content), code)

  return make_response(jsonify(get_user_by_uuid(uuid)[0]), 200)

@app.route('<uuid>/visit/<place_uid>/', methods=['POST'])
def visit_place(uuid, place_uid):
  # API Token exist?
  if 'X_API_Token' not in request.headers:
    return make_response(jsonify({'message': 'API token not found'}), 400)
  # API Token Correct?
  if not check_api_token(request.headers['X_API_Token']):
    return make_response(jsonify({'message': 'API token is not correct'}), 400)

  user_records = get_user_by_uuid(uuid)
  if len(user_records) == 0:
    return make_response(jsonify({'message': 'No user found on specified uuid'}), 400)

  visit(user_records[0]['id'], place_uid)


  return make_response(jsonify({'message': '{} visited at {}'.format(uuid, place_uid)}), 200)

@app.route('<uuid>/visit-history/', methods=['GET'])
def get_visit_history(uuid):
  # API Token exist?
  if 'X_API_Token' not in request.headers:
    return make_response(jsonify({'message': 'API token not found'}), 400)
  # API Token Correct?
  if not check_api_token(request.headers['X_API_Token']):
    return make_response(jsonify({'message': 'API token is not correct'}), 400)

  user_records = get_user_by_uuid(uuid)
  if len(user_records) == 0:
    return make_response(jsonify({'message': 'No user found on specified uuid'}), 400)

  result = visit_history(user_records[0]['id'])

  if len(result) == 0:
    return '', 204
  else:
    return make_response(jsonify(result), 200)