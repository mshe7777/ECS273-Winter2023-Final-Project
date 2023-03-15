from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from controller import get_months
import numpy as np
import json

app = Flask(__name__)
CORS(app)

@app.route("/")
@cross_origin()
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/basic/monthList")
@cross_origin()
def monthList():
    month_list = get_months()
    month_list2 = np.array(month_list, dtype=str).tolist()
    return json.dumps({'monthList': month_list2})

if __name__ == "__main__":
    app.run(port=3100, debug=True)