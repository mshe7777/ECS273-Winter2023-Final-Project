from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from pandas._libs.tslibs.period import Period
from data_process.load_data import init
from controller import get_months, get_temporal_user_statistics, query_rating_records, monthly_degree_distribution, \
    rating_score_distribution, user_monthly_degree, save_raw_data_to_file, user_monthly_degree_flattened, \
    get_statistic_data
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
def fetch_month_list():
    month_list = get_months()
    month_list2 = np.array(month_list, dtype=str).tolist()
    return json.dumps({'monthList': month_list2})


@app.route("/temporal/userRatingStatistics/<month>")
@cross_origin()
def temporal_user_rating_statistics(month):
    # step 0. request parameter correction
    month_period = get_month_period(month)
    # step 1. get user temporally statistic data
    user_statistic_list = get_temporal_user_statistics(month_period)
    # step 2. rating records
    record_list = query_rating_records(month_period)
    # step 3. get_statistic_data
    statis_data = get_statistic_data(user_statistic_list)
    # step 4. merge and generate result string
    return json.dumps({'nodes': user_statistic_list, 'links': record_list, 'statistic': statis_data})


@app.route("/temporal/degreeDistribution/<month>")
@cross_origin()
def temporal_degree_distribution(month):
    month_period = get_month_period(month)
    dictList = monthly_degree_distribution(month_period)
    return json.dumps({'data': dictList})


@app.route("/temporal/ratingDistribution/<month>")
@cross_origin()
def rating_distribution(month):
    month_period = get_month_period(month)
    dictList = rating_score_distribution(month_period)
    return json.dumps({'data': dictList})


@app.route("/temporal/user/monthlyDegree/<user_id>/<month>")
@cross_origin()
def monthly_degree(user_id, month):
    month_period = None
    if month == '-1':
        month_period = get_months()[-1]
    else:
        month_period = Period(month)

    dictList = user_monthly_degree(user_id, month_period)
    return json.dumps({'data': dictList})


@app.route("/temporal/user/monthlyDegreeFlatterned/<user_id>/<month>")
@cross_origin()
def monthly_degree_flat(user_id, month):
    month_period = None
    if month == '-1':
        month_period = get_months()[-1]
    else:
        month_period = Period(month)

    dictList = user_monthly_degree_flattened(user_id, month_period)
    return json.dumps({'data': dictList})


@app.route("/file/generate")
@cross_origin()
def generate_file():
    save_raw_data_to_file()
    return json.dumps({'result': 'done'})


def get_month_period(month):
    if month == '0':
        return get_months()[0]
    else:
        return Period(month)


if __name__ == "__main__":
    init("./data/soc-sign-bitcoinotc.csv")
    app.run(port=3100, debug=True)
