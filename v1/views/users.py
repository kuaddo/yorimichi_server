from models.users import create_user, get_posts_by_uuid

from flask import Blueprint, jsonify, make_response, request

app = Blueprint('users', __name__, url_prefix='/v1/users')

@app.route('/', methods=['GET', 'POST'])
def index():
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
    return make_response(jsonify({'message': 'No Posts'}), 204)