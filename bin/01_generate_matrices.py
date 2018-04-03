"""Split ill-formed and heavy JSON into many smaller files."""
import fire
import os
import glob
import json
import nltk
from collections import Counter, defaultdict
import itertools
import pandas as pd
import multiprocessing
from contrastes.processing import build_province_df


def generate_matrices(num_files=5):
    df = pd.DataFrame()
    for province in ["buenosaires", "larioja", "tucuman"]:
        jsons = os.path.join("data/tweets", province, "*.json")

        jsons = glob.glob(jsons)[:4]

        province_df = build_province_df(province, jsons)

        df = df.add(province_df, fill_value=.0)

    df.to_csv("matrix.csv")

if __name__ == '__main__':
    fire.Fire(generate_matrices)
