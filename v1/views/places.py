from models.posts import get_posts_by_place

from flask import Blueprint, jsonify, make_response, request

app = Blueprint('places', __name__, url_prefix='/v1/places')

@app.route('/<place_uid>/posts/', methods=['GET'])
def posts(place_uid):
  res = get_posts_by_place(place_uid)

  if len(res) > 0:
    return make_response(jsonify({'message': 'Request Completed.', 'posts_array': res}), 200)
  else:
    return make_response(jsonify({'message': 'No posts.'}), 204)