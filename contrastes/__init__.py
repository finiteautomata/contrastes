
import re
import pandas as pd


def read_occurrence_dataframe(path, filter_words=False):
    df = pd.read_csv(path, index_col=0)
    cant_palabras = [c for c in df.columns if re.match(r'.*ocurrencias$', c)]
    cant_personas = [c for c in df.columns if re.match(r'.*usuarios$', c)]

    df["cant_provincias"] = (df[cant_palabras] > 0).sum(axis=1)
    df["cant_palabra"] = df[cant_palabras].sum(axis=1)
    df["cant_usuarios"] = df[cant_personas].sum(axis=1)

    df = df.loc[df.index.notnull()]

    if filter_words:
        df = df[(df.cant_palabra >= 100) & (df.cant_usuarios >= 25) ]

    df.cant_palabras = cant_palabras
    df.cant_personas = cant_personas

    return df
