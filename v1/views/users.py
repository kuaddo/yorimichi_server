from flask import Blueprint, jsonify, make_response

app = Blueprint('users', __name__, url_prefix='/v1/users')

@app.route('/')
def index():
  return make_response(jsonify({'message': 'This is user view root'}))