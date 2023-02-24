from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)

@app.route("/")
@cross_origin()
def hello_world():
    return "<p>Hello, World!</p>"


if __name__ == "__main__":
    app.run(port=3100, debug=True)