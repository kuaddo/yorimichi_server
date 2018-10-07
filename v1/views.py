from flask import Blueprint, jsonify, make_response

v1 = Blueprint('v1', __name__, url_prefix='/v1')

@v1.route('/')
def index():
  return make_response(jsonify({'message': 'This is v1 API root'}))