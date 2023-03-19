import pandas as pd
import numpy as np
from pandas._libs.tslibs.period import Period
import os
from data_process.load_data import init, get_month_list, get_basic_dataframe
import json


def get_months():
    return get_month_list()


def get_temporal_user_statistics(parameter_month):
    df_basic_immutable = get_basic_dataframe()
    # filtering df using specified month
    filtered3 = df_basic_immutable[df_basic_immutable.datetime_typed.dt.to_period('M') == parameter_month]
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
    merged = pd.merge(indegree_filterd, outdegree_filterd, on='id', how='outer')
    merged = merged.replace(np.nan, 0)
    # converting the dataframe to List
    return merged.to_dict('records')


def get_statistic_data(dict_list):
    # extract statistic inside the nodes list
    if len(dict_list) == 0:
        return {'minCountIn': 0, 'maxCountIn': 0, 'minCountOut': 0, 'maxCountOut': 0, 'minSumRatingIn': 0, 'maxSumRatingIn': 0}

    statis_dict = {'minCountIn': 100000, 'maxCountIn': 0,
                   'minCountOut': 1000000, 'maxCountOut': 0,
                   'minSumRatingIn': 10000000, 'maxSumRatingIn': 0}
    for tempRow in dict_list:
        if tempRow['incoming'] < statis_dict['minCountIn']:
            statis_dict['minCountIn'] = tempRow['incoming']
        if tempRow['incoming'] > statis_dict['maxCountIn']:
            statis_dict['maxCountIn'] = tempRow['incoming']

        if tempRow['outgoing'] < statis_dict['minCountOut']:
            statis_dict['minCountOut'] = tempRow['outgoing']
        if tempRow['outgoing'] > statis_dict['maxCountOut']:
            statis_dict['maxCountOut'] = tempRow['outgoing']

        if tempRow['in_rating_sum'] < statis_dict['minSumRatingIn']:
            statis_dict['minSumRatingIn'] = tempRow['in_rating_sum']
        if tempRow['in_rating_sum'] > statis_dict['maxSumRatingIn']:
            statis_dict['maxSumRatingIn'] = tempRow['in_rating_sum']

    return statis_dict


def query_rating_records(parameter_month):
    df_basic_immutable = get_basic_dataframe()
    # filtering df using specified month
    filtered3 = df_basic_immutable[df_basic_immutable.datetime_typed.dt.to_period('M') == parameter_month]
    filtered3.reset_index()

    # searching the wanted rating list
    filtered3 = df_basic_immutable[df_basic_immutable.datetime_typed.dt.to_period('M') == parameter_month]
    filtered3.reset_index()
    filtered3 = filtered3.rename(columns={'datetime': 'time'})
    return filtered3[['source', 'target', 'rating', 'time']].to_dict('records')


def monthly_degree_distribution(month_parameter):
    df_basic_immutable = get_basic_dataframe()
    monthFilteredDf = df_basic_immutable[df_basic_immutable.datetime_typed.dt.to_period('M') == month_parameter]
    monthFilteredDf.reset_index()
    # group by month
    monthFilteredDf['datetime_typed'] = monthFilteredDf['datetime_typed'].dt.strftime('%m-%d')
    monthGroupedDf = monthFilteredDf.groupby('datetime_typed').agg({'rating': 'size'}).reset_index()
    monthGroupedDf = monthGroupedDf.rename(columns={'datetime_typed': 'time', 'rating': 'edgeNumber'})

    return monthGroupedDf.to_dict('records')


def rating_score_distribution(month_parameter):
    df_basic_immutable = get_basic_dataframe()
    monthFilteredDf = df_basic_immutable[df_basic_immutable.datetime_typed.dt.to_period('M') == month_parameter]
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
        ratingGroupedDf.loc[len(ratingGroupedDf.index)] = [missing_month, 0]

    while max_rating < 10:
        max_rating = max_rating + 1
        ratingGroupedDf.loc[len(ratingGroupedDf.index)] = [max_rating, 0]

    ratingGroupedDf = ratingGroupedDf.sort_values(by=['rating'])
    ratingGroupedDf = ratingGroupedDf.reset_index(drop=True)
    ratingGroupedDf = ratingGroupedDf.rename(columns={'rating': 'edgeRating', 'source': 'frequency'})
    return ratingGroupedDf.to_dict('records')


def user_monthly_degree(user_id, month_period):
    df_basic_immutable = get_basic_dataframe()
    # filter by given month
    monthFilteredDf4 = df_basic_immutable[df_basic_immutable.datetime_typed.dt.to_period('M') == month_period]

    monthFilteredDf4 = monthFilteredDf4[
        (monthFilteredDf4['source'] == user_id) | (monthFilteredDf4['target'] == user_id)]
    monthFilteredDf4.reset_index(drop=True)
    # convert date column to the type of Period(freq='M')
    monthFilteredDf4['datetime_typed'] = monthFilteredDf4['datetime_typed'].dt.strftime('%m-%d')
    # filter by given user_id as source
    outgoingFilteredDf = monthFilteredDf4[monthFilteredDf4['source'] == user_id]
    outgoingFilteredDf = outgoingFilteredDf.groupby('datetime_typed').agg({'target': 'size'}).reset_index()
    outgoingFilteredDf = outgoingFilteredDf.rename(columns={'datetime_typed': 'month', 'target': 'outgoing'})
    # filter by given user_id as target
    incomingFilteredDf = monthFilteredDf4[monthFilteredDf4['target'] == user_id]
    incomingFilteredDf = incomingFilteredDf.groupby('datetime_typed').agg({'source': 'size'}).reset_index()
    incomingFilteredDf = incomingFilteredDf.rename(columns={'datetime_typed': 'month', 'source': 'incoming'})
    mergedUserDf = pd.merge(outgoingFilteredDf, incomingFilteredDf, how='outer', on='month', )
    mergedUserDf = mergedUserDf.replace(np.nan, 0)
    mergedUserDf[['outgoing', 'incoming']] = mergedUserDf[['outgoing', 'incoming']].astype(int)
    mergedUserDf['month'] = mergedUserDf.month.astype(str)
    return mergedUserDf.to_dict('records')


def user_monthly_degree_flattened(user_id, month_period):
    df_basic_immutable = get_basic_dataframe()
    # filter by given month
    monthFilteredDf4 = df_basic_immutable[df_basic_immutable.datetime_typed.dt.to_period('M') == month_period]

    monthFilteredDf4 = monthFilteredDf4[
        (monthFilteredDf4['source'] == user_id) | (monthFilteredDf4['target'] == user_id)]
    monthFilteredDf4.reset_index(drop=True)
    # convert date column to the type of Period(freq='M')
    monthFilteredDf4['datetime_typed'] = monthFilteredDf4.datetime_typed.dt.to_period('M')
    # filter by given user_id as source
    outgoingFilteredDf = monthFilteredDf4[monthFilteredDf4['source'] == user_id]
    outgoingFilteredDf = outgoingFilteredDf.groupby('datetime_typed').agg({'target': 'size'}).reset_index()
    outgoingFilteredDf = outgoingFilteredDf.rename(columns={'datetime_typed': 'month', 'target': 'frequence'})
    outgoingFilteredDf['type'] = 'outgoing'

    # filter by given user_id as target
    incomingFilteredDf = monthFilteredDf4[monthFilteredDf4['target'] == user_id]
    incomingFilteredDf = incomingFilteredDf.groupby('datetime_typed').agg({'source': 'size'}).reset_index()
    incomingFilteredDf = incomingFilteredDf.rename(columns={'datetime_typed': 'month', 'source': 'frequence'})
    incomingFilteredDf['type'] = 'incoming'

    concatFrames = [incomingFilteredDf, outgoingFilteredDf]
    resultFrame = pd.concat(concatFrames)
    resultFrame['month'] = resultFrame.month.astype(str)

    return resultFrame.to_dict('records')


def save_raw_data_to_file():
    basic_dataframe = get_basic_dataframe()
    if os.path.exists("./export_dataframe.json"):
        os.remove("./export_dataframe.json")

    basic_dataframe.to_json(r'./export_dataframe.json', orient='records')


if __name__ == "__main__":
    init("./data/soc-sign-bitcoinotc.csv")
    dict = user_monthly_degree('2',Period('2011-02'))
    print(dict)