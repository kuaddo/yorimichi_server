from utils.cloud_storage_manager import uploadPost, downloadPost
from models.users import get_user
from models.posts import create

from flask import Blueprint, jsonify, make_response, request

app = Blueprint('posts', __name__, url_prefix='/v1/posts/')

@app.route('/', methods=['POST'])
def create_post():
  if request.headers['Content-Type'] != 'application/json':
    return make_response(jsonify({'message': 'error'}), 400)

  json = request.json
  if not ('b64image' in json and 'place_uid' in json and 'uuid' in json):
    return make_response(jsonify({'message': 'Require b64, place_uid, uuid.'}), 400)
  
  # get user_id from uuid
  user_records = get_user(json['uuid'])
  if len(user_records) == 0:
    return make_response(jsonify({'message': 'uuid not found.'}), 400)

  user_id = user_records[0]['id']

  # upload
  ret = uploadPost(json['b64image'], user_id)

  # create record
  create(ret['cloud_storage_filename'], user_id, json['place_uid'])

  return make_response(jsonify({'message': 'Successfuly Uploaded.'}))