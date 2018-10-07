from flask import Flask, jsonify, make_response
from v1.views import app_list

app = Flask(__name__)

for child_app in app_list:
  app.register_blueprint(child_app)

@app.route('/')
def index():
  return make_response(jsonify({'message': 'This is API root'}))

if __name__ == '__main__':
  app.run(debug=True)