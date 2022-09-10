def is_data_null(data):
    pass


def position_formatter(df):
    cols = df.columns
    df = df.T
    df['symbols'] =  cols
    return df