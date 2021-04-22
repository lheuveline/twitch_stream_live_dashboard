import pandas as pd

def get_raw_stream(df):

    return pd.DataFrame \
        .from_records(df[1].values) \
        .to_json(orient = "records")

def extract_top_categories(df):

    # Preprocessing needed 
    # TO-DO : get table schema from redis

    df[1] = df[1].apply(lambda x: x[b"count"].decode()).astype(float)

    return df \
        .sort_values(1, ascending = False) \
        .loc[df[1] > df[1].quantile(0.9)] \
        .reset_index(drop = True)

def wordcount(df):

    # Preprocessing needed 
    # TO-DO : get table schema from redis

    df[1] = df[1].apply(lambda x: x[b"count"].decode()).astype(float)

    # return df \
    #     .loc[df[1] > 1] \
    #     .sort_values(1, ascending = False) \
    #     .reset_index(drop = True) \
    #     .to_json()

    return df \
        .loc[df[1] > 1] \
        .set_index(0)[1].to_dict()