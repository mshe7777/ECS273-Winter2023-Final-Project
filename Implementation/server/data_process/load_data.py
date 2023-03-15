import pandas as pd
import numpy as np
import json

# Constants area

file_name = '../data/soc-sign-bitcoinotc.csv'
file_name_alpha = "../data/soc-sign-bitcoinalpha.csv"

# globally basic underlying raw dataFrame
df_basic_immutable = None

MONTH_LIST = None


def get_month_list():
    return MONTH_LIST.copy()


# define the function loading data from target file
def init():
    columns = ['source', 'target', 'rating', 'datetime']
    df = pd.read_csv(file_name, names=columns, header=None,
                     dtype={"source": str, "target": str, "rating": int}, )
    # to convert the given seconds of epoch with decimal value to a datetime
    df['datetime'] = df['datetime'].astype(int)
    df['datetime_typed'] = pd.to_datetime(df['datetime'], unit='s')

    global df_basic_immutable
    df_basic_immutable = df

    # step 1: filter by specified user id list.
    user_id_list = __get_user_list()
    df = df[df.source.isin(user_id_list) & df.target.isin(user_id_list)]
    # step 2: further filter by month list
    __get_month_list()
    df = df[df.datetime_typed.dt.to_period('M').isin(MONTH_LIST)]



# inner method,shouldn't be invoked from any outer code
def __get_user_list():
    global df_basic_immutable
    # out-degree statistics
    groupedRaterDF = df_basic_immutable.groupby('source').agg({'rating': 'size'}).reset_index()
    groupedRaterDF.sort_values('rating', ascending=False, inplace=True)
    # in-degree statistics
    groupedRateeDF = df_basic_immutable.groupby('target').agg({'rating': 'size'}).reset_index()
    groupedRateeDF.sort_values('rating', ascending=False, inplace=True)

    # merge in and out degrees
    mergedDF = pd.merge(groupedRaterDF, groupedRateeDF.rename(columns={'target': 'source'}), on='source',
                        suffixes=('_out', '_in'))
    sorted_indices = (mergedDF["rating_out"] + mergedDF["rating_in"]).sort_values(ascending=False).index
    mergedDF.rename(columns={'source': 'user_id'}, inplace=True)
    mergedDF = mergedDF.loc[sorted_indices, :]
    mergedDF = mergedDF.query("rating_out+rating_in >= 40")
    mergedDF = mergedDF.sample(n=300)

    # sort the sampled dataframe according to sum(rating_out+rating_int) descendingly.
    # sorted_indices2 = (mergedDF["rating_out"] + mergedDF["rating_in"]).sort_values(ascending=False).index
    # mergedDF = mergedDF.loc[sorted_indices2, :]

    user_id_list = mergedDF['user_id'].to_list()

    # df_filtered = df.query('source in @user_id_list or target in @user_id_list')
    return user_id_list


# inner method,shouldn't be invoked from any outer code
def __get_month_list():
    global df_basic_immutable
    global MONTH_LIST
    dateGroupedDF = df_basic_immutable.groupby(df_basic_immutable.datetime_typed.dt.to_period("M")).agg(
        {'rating': 'size'}).reset_index()
    dateGroupedDF = dateGroupedDF.query('rating>50 and rating <700')

    # randomly sampling the dataframe
    # dateGroupedDF = dateGroupedDF.query('rating >= 30')
    # dateGroupedDF = dateGroupedDF.sample(n=30,random_state=1)

    dateGroupedDF = dateGroupedDF.sort_values('datetime_typed', ascending=True)
    MONTH_LIST = dateGroupedDF['datetime_typed'].to_list()


if __name__ == "__main__":
    init()
    month_list2 = np.array(MONTH_LIST, dtype=str).tolist()
    strs = json.dumps({'monthList': month_list2})
    print(strs)
