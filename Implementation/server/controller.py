import pandas as pd
import numpy as np
from pandas._libs.tslibs.period import Period

from data_process.load_data import init, get_month_list, get_basic_dataframe
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


def monthly_degree_distribution(month_parameter):
    df_basic_immutable = get_basic_dataframe()
    monthFilteredDf = df_basic_immutable[df_basic_immutable.datetime_typed.dt.to_period('M') <= month_parameter]
    monthFilteredDf['datetime_typed'] = monthFilteredDf.datetime_typed.dt.to_period('M')
    monthFilteredDf.reset_index()
    monthFilteredDf
    # group by month
    monthGroupedDf = monthFilteredDf.groupby('datetime_typed').agg({'rating': 'size'}).reset_index()
    monthGroupedDf = monthGroupedDf.rename(columns={'datetime_typed': 'time', 'rating': 'edgeNumber'})
    return monthGroupedDf.to_dict('records')


def rating_score_distribution(month_parameter):
    df_basic_immutable = get_basic_dataframe()
    monthFilteredDf = df_basic_immutable[df_basic_immutable.datetime_typed.dt.to_period('M') <= month_parameter]
    # group data according to rating scores
    ratingGroupedDf = monthFilteredDf.groupby('rating').agg({'source': 'size'}).reset_index()

    last_rating = -11
    supplement_list = []
    max_rating = -11
    for index, row in ratingGroupedDf.iterrows():
        current_rating = row['rating']
        max_rating = current_rating

        while current_rating - last_rating > 1:
            last_rating = last_rating + 1
            supplement_list.append(last_rating)
        last_rating = last_rating + 1

    # supplement_list

    for missing_month in supplement_list:
        if missing_month == 0:
            continue
        ratingGroupedDf.loc[len(ratingGroupedDf.index)] = [missing_month, 0]

    while max_rating < 10:
        max_rating = max_rating + 1
        ratingGroupedDf.loc[len(ratingGroupedDf.index)] = [max_rating, 0]

    ratingGroupedDf = ratingGroupedDf.sort_values(by=['rating'])
    ratingGroupedDf = ratingGroupedDf.reset_index(drop=True)
    ratingGroupedDf = ratingGroupedDf.rename(columns={'rating': 'edgeRating', 'source': 'frequency'})
    return ratingGroupedDf.to_dict('records')


if __name__ == "__main__":
    init("./data/soc-sign-bitcoinotc.csv")
    dictList = rating_score_distribution(Period('2012-03'))
    print(dictList)
