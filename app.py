from flask import Flask, jsonify, make_response
from v1.views import v1

app = Flask(__name__)

app.register_blueprint(v1)

@app.route('/')
def index():
  return make_response(jsonify({'message': 'This is API root'}))

if __name__ == '__main__':
  app.run(debug=True)