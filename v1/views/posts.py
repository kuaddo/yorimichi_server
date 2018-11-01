from utils.cloud_storage_manager import uploadPost, downloadPost
from utils.apitoken import check_api_token
from models.users import get_user_by_uuid
from models.posts import create

from flask import Blueprint, jsonify, make_response, request

app = Blueprint('posts', __name__, url_prefix='/v1/posts/')

@app.route('/', methods=['POST'])
def create_post():
  # API Token exist?
  if 'X_API_Token' not in request.headers:
    return make_response(jsonify({'message': 'API token not found'}), 400)
  # API Token Correct?
  if not check_api_token(request.headers['X_API_Token']):
    return make_response(jsonify({'message': 'API token is not correct'}), 400)
  # When multipule Content-Type Specified, 'application/json' != request.headers['Content-Type'] is True.
  # So, split request.headers['Content-Type'] to list by ';'.
  if 'application/json' not in  request.headers['Content-Type'].split(';'):
    return make_response(jsonify({'message': 'error'}), 400)

  json = request.json
  if not ('b64image' in json and 'place_uid' in json and 'uuid' in json):
    return make_response(jsonify({'message': 'Require b64, place_uid, uuid.'}), 400)
  
  # get user_id from uuid
  user_records = get_user_by_uuid(json['uuid'])
  if len(user_records) == 0:
    return make_response(jsonify({'message': 'uuid not found.'}), 400)

  user_id = user_records[0]['id']

  # upload
  ret = uploadPost(json['b64image'], user_id)

  # create record
  create(ret['cloud_storage_filename'], user_id, json['place_uid'])

  return make_response(jsonify({'message': 'Successfuly Uploaded.'}))
