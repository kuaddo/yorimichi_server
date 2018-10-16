from models.users import create_user

from flask import Blueprint, jsonify, make_response, request

app = Blueprint('users', __name__, url_prefix='/v1/users')

@app.route('/', methods=['GET', 'POST'])
def index():
  if request.method == 'POST':
    uuid = create_user()
    return make_response(jsonify({'message': 'Create User.', 'uuid': uuid}))
  else:
    return make_response(jsonify({'message': 'This is user view root'}))