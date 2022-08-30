import pandas as pd


def preprocess(df,region_df):
    #filtering summer athlete
    df = df[df['Season'] == 'Summer']

    #merging with region
    df = df.merge(region_df, on='NOC', how='left')

    #droping duplicates
    df.drop_duplicates(inplace=True)

    #one hot encoding
    df = pd.concat([df, pd.get_dummies(df['Medal'])], axis=1)

    return df