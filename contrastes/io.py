"""Module in charge of input output"""
import pandas as pd
import re


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
    cant_palabras = [c for c in df.columns if re.match(r'.*ocurrencias$', c)]
    cant_personas = [c for c in df.columns if re.match(r'.*usuarios$', c)]

    df["cant_provincias"] = (df[cant_palabras] > 0).sum(axis=1)
    df["cant_palabra"] = df[cant_palabras].sum(axis=1)
    df["cant_usuarios"] = df[cant_personas].sum(axis=1)

    df = df.loc[df.index.notnull()]

    if filter_words:
        min_words, min_users = 40, 25
        if isinstance(filter_words, tuple):
            min_words = filter_words[0]
            min_users = filter_words[1]

        df = df[(df.cant_palabra >= min_words) &
                (df.cant_usuarios >= min_users)]

    df.cant_palabras = cant_palabras
    df.cant_personas = cant_personas

    return df
