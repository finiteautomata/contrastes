
import re
import pandas as pd


def read_occurrence_dataframe(path):
    df = pd.read_csv(path, index_col=0)
    cant_palabras = [c for c in df.columns if re.match(r'.*ocurrencias$', c)]
    cant_personas = [c for c in df.columns if re.match(r'.*usuarios$', c)]

    df["cant_provincias"] = (df[cant_palabras] > 0).sum(axis=1)
    df["cant_palabra"] = df[cant_palabras].sum(axis=1)
    df["cant_usuarios"] = df[cant_personas].sum(axis=1)

    return df
