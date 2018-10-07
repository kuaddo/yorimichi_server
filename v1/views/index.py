from flask import Blueprint, jsonify, make_response

app = Blueprint('index', __name__, url_prefix='/v1')

@app.route('/')
def index():
  return make_response(jsonify({'message': 'This is v1 API root'}))