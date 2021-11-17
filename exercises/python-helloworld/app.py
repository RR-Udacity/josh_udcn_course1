from flask import Flask
from flask import jsonify, request
import json
import logging
import os

# filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'app.log')
logging.basicConfig(filename="app.log", level=logging.DEBUG)

app = Flask(__name__)

@app.route("/", methods=["GET"])
def hello():
    return "Hello World!"

# Metrics Endpoint
@app.route('/metrics', methods=["GET"])
def metrics():
    response = app.response_class(
        response=json.dumps({"status": "success", "code": 0, "data": {"UserCount": 140, "UserCountActive": 123}}),
        status=200,
        mimetype='application/json'
    )
    if request.method == 'GET':
        app.logger.info('Metrics request successful')
        return response

# Status Endpoint
@app.route('/status', methods=["GET"])
def status():
    resp = "OK - healthy"

    data = dict(
        result= resp
    )
    if request.method == 'GET':
        app.logger.info('Status request successful')
        return jsonify(data)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
