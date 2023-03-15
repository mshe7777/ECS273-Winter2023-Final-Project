import pandas as pd
import numpy as np
from pandas._libs.tslibs.period import Period

from data_process.load_data import init,get_month_list, get_basic_dataframe
import json

def get_months():
    return get_month_list()


def get_temporal_user_statistics(parameter_month):
    df_basic_immutable = get_basic_dataframe()
    # filtering df using specified month
    filtered3 = df_basic_immutable[df_basic_immutable.datetime_typed.dt.to_period('M') <= parameter_month]
    filtered3.reset_index()

    # group df according to in-degree and out-degree respectively
    # in-degree
    outdegree_filterd = filtered3.groupby('source').agg({'target': 'size', 'rating': 'sum'}).reset_index()
    outdegree_filterd.rename(columns={'source': 'id', 'target': 'outgoing', 'rating': 'out_rating_sum'},
                             inplace=True)
    # out-degree
    indegree_filterd = filtered3.groupby('target').agg({'source': 'size', 'rating': 'sum'}).reset_index()
    indegree_filterd.rename(columns={'target': 'id', 'source': 'incoming', 'rating': 'in_rating_sum'},
                            inplace=True)
    # the dataframe after merging
    merged = pd.merge(indegree_filterd, outdegree_filterd, on='id')

    # converting the dataframe to List
    return merged.to_dict('records')


def query_rating_records(parameter_month):
    df_basic_immutable = get_basic_dataframe()
    # filtering df using specified month
    filtered3 = df_basic_immutable[df_basic_immutable.datetime_typed.dt.to_period('M') <= parameter_month]
    filtered3.reset_index()

    # searching the wanted rating list
    filtered3 = df_basic_immutable[df_basic_immutable.datetime_typed.dt.to_period('M') <= parameter_month]
    filtered3.reset_index()
    filtered3 = filtered3.rename(columns={'datetime': 'time'})
    return filtered3[['source', 'target', 'rating', 'time']].to_dict('records')


def test(month):
    # step 0. request parameter correction
    month_period = None
    if month == '0':
        month_period = get_months()[0]
    else:
        month_period = Period(month)

    # step 1. get user temporally statistic data
    user_statistic_list = get_temporal_user_statistics(month_period)
    # step 2. rating records
    record_list = query_rating_records(month_period)
    # step 3. merge and generate result string
    return json.dumps({'nodes': user_statistic_list, 'links': record_list})


if __name__ == "__main__":
    init("./data/soc-sign-bitcoinotc.csv")
    strResult = test('0')
    print(strResult)