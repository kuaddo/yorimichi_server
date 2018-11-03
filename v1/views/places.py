from models.posts import get_posts_by_place
from utils.apitoken import check_api_token
from utils.api_wrapper import bykeyword, bytype, nextpage

from flask import Blueprint, jsonify, make_response, request, Response

app = Blueprint('places', __name__, url_prefix='/v1/places')

@app.route('/<place_uid>/posts/', methods=['GET'])
def posts(place_uid):
  # API Token exist?
  if 'X_API_Token' not in request.headers:
    return make_response(jsonify({'message': 'API token not found'}), 400)
  # API Token Correct?
  if not check_api_token(request.headers['X_API_Token']):
    return make_response(jsonify({'message': 'API token is not correct'}), 400)
  res = get_posts_by_place(place_uid)

  if len(res) > 0:
    return make_response(jsonify({'message': 'Request Completed.', 'posts_array': res}), 200)
  else:
    return '', 204

@app.route('/searchbytype/', methods=['GET'])
def getbytype():
  # API Token exist?
  if 'X_API_Token' not in request.headers:
    return make_response(jsonify({'message': 'API token not found'}), 400)
  # API Token Correct?
  if not check_api_token(request.headers['X_API_Token']):
    return make_response(jsonify({'message': 'API token is not correct'}), 400)

  params = request.args
  location = params.get('location')
  radius = params.get('radius')
  type_value = params.get('type')
  if location is None:
    return make_response(jsonify({'message': 'Missing parameter \'location\''}), 400)
  if radius is None:
    return make_response(jsonify({'message': 'Missing parameter \'radius\''}), 400)
  if type_value is None:
    return make_response(jsonify({'message': 'Missing parameter \'type\''}), 400)
  
  content, code = bytype(location, radius, type_value)
  return make_response(Response(content, headers={'Content-Type': 'application/json'}), code)

@app.route('/searchbykeyword/', methods=['GET'])
def getbykeyword():
  # API Token exist?
  if 'X_API_Token' not in request.headers:
    return make_response(jsonify({'message': 'API token not found'}), 400)
  # API Token Correct?
  if not check_api_token(request.headers['X_API_Token']):
    return make_response(jsonify({'message': 'API token is not correct'}), 400)

  params = request.args
  location = params.get('location')
  radius = params.get('radius')
  keyword = params.get('keyword')
  
  if location is None:
    return make_response(jsonify({'message': 'Missing parameter \'location\''}), 400)
  if radius is None:
    return make_response(jsonify({'message': 'Missing parameter \'radius\''}), 400)
  if keyword is None:
    return make_response(jsonify({'message': 'Missing parameter \'keyword\''}), 400)

  content, code = bykeyword(location, radius, keyword)
  return make_response(Response(content, headers={'Content-Type': 'application/json'}), code)

@app.route('/getnext/', methods=['GET'])
def next():
  # API Token exist?
  if 'X_API_Token' not in request.headers:
    return make_response(jsonify({'message': 'API token not found'}), 400)
  # API Token Correct?
  if not check_api_token(request.headers['X_API_Token']):
    return make_response(jsonify({'message': 'API token is not correct'}), 400)

  params = request.args
  return make_response(jsonify({'message': 'next Token',
                                'nextToken': params['nextToken']}), 200)