import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

def preprocess(df):
    dt = pd.get_dummies(df,drop_first=True)

    return dt








