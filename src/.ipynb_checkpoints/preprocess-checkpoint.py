""" Preprocessing pipeline for sample dataset """

import pandas as pd

def new_features(df):
    """
    Adds proposed new features to raw input dataframe
    add a small float to avoid inf values

    Args:
        df (pd.DataFrame): The input DataFrame

    Returns:
        pd.DataFrame: Expanded dataframe with new features
    """
    df['bal_vol_index'] = df['BalanceMin']/(df['BalanceAverage'] + .000001)

    df['dep_wd_ratio'] = df['AverageMonthlySpend']/(df['AverageMonthlyIncome'] + .000001)

    df['od_per_30d'] = df['OverdraftCount']/(df['TotalHistoryInDays']/30)

    return df


def imputation(df):
    """
    Imputes missing values with zero and adds a missing indicator column for each column
    that had missing values.

    Args:
        df (pd.DataFrame): The input DataFrame.

    Returns:
        pd.DataFrame: The DataFrame with missing values imputed and indicator columns added.
    """
    df_processed = df.copy()
    for col in df_processed.columns:
        if df_processed[col].isnull().any():
            df_processed[f'{col}_missing'] = df_processed[col].isnull().astype(int)
            df_processed[col] = df_processed[col].fillna(0)
    return df_processed


def one_hot_encode_paycheck_model(df):
    """
    One-hot encodes the 'PaycheckModelUsed' column in the raw data.
    
    Parameters:
    df (pd.DataFrame): The input DataFrame with the 'PaycheckModelUsed' column.

    Returns:
    pd.DataFrame: A new DataFrame with one-hot encoded 'PaycheckModelUsed' columns.
    """
    return pd.get_dummies(df, 
                          columns=["PaycheckModelUsed"], 
                          prefix="PaycheckModel", 
                          drop_first=True,
                          dtype='int64')


def preprocess(df):
    """
    Runs full data preparation pipeline
    """
    df_new = new_features(df)

    df_imputed = imputation(df_new)

    df_final = one_hot_encode_paycheck_model(df_imputed)

    return df_final