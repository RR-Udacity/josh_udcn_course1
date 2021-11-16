from flask import Flask
from flask import jsonify, request
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

if __name__ == "__main__":
    app.run(host='0.0.0.0')

# Metrics Endpoint
@app.route('/metrics', methods=["GET"])
def metrics():
    resp = dict(
        UserCount = 140,
        UserCountActive = 23
    )
    data = dict(
        data= resp
    )
    if request.method == 'GET':
        return jsonify(data)
    
# Status Endpoint
@app.route('/status', methods=["GET"])
def status():
    resp = "OK - healthy"

    data = dict(
        result= resp
    )
    if request.method == 'GET':
        return jsonify(data)