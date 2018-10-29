from models.posts import get_posts_by_place

from flask import Blueprint, jsonify, make_response, request

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