"""Module in charge of input output"""
import pandas as pd
from .processing import preprocess_raw_df

def read_occurrence_dataframe(path, filter_words=None):
    """
    Read word-provinces dataframe.

    Parameters:
    -----------

    path: string or any object responding to read()
        Path to .csv file

    filter_words: Bool or tuple (no_occurrences, no_users)
    """
    df = pd.read_csv(path, index_col=0)

    df = preprocess_raw_df(df, filter_words)

    return df
