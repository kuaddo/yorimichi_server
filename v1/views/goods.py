from models.goods import get_icon
from utils.apitoken import check_api_token

from flask import Blueprint, jsonify, make_response, request

app = Blueprint('goods', __name__, url_prefix='/v1/goods')

@app.route('/icons/<icon_id>/', methods=['GET'])
def icon(icon_id):
  # API Token exist?
  if 'X_API_Token' not in request.headers:
    return make_response(jsonify({'message': 'API token not found'}), 400)
  # API Token Correct?
  if not check_api_token(request.headers['X_API_Token']):
    return make_response(jsonify({'message': 'API token is not correct'}), 400)

  ret = get_icon(icon_id)

  if len(ret) == 0:
    return make_response(jsonify({'message': 'Icon not found, check request parameter.'}), 400)
  if len(ret) == 1:
    return make_response(jsonify(ret[0]), 200)
