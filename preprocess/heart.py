import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

def preprocess(df):
    df[df['sex'] == 'male'] = 1
    df[df['sex'] == 'female'] = 0
    dt = pd.get_dummies(df)

    return dt








