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
from contrastes.processing import tokenize, get_counters, merge_counters


def _get_counters_from_file(json_path):
    return get_counters(json.load(open(json_path)))


def get_province_df(province_name, jsons, no_workers=4):
    """
    Creates dataframe for a Province
    """
    print("Processing {}".format(province_name))
    pool = multiprocessing.Pool(no_workers, maxtasksperchild=1)

    fds, user_counters = zip(*pool.map(_get_counters_from_file, jsons))
    fd, users = merge_counters(fds, user_counters)

    users_occurrences = {k:len(v) for k, v in users.items()}

    occurrences_column = "{}_ocurrencias".format(province_name)
    users_column = "{}_usuarios".format(province_name)

    print("Done. Building dataframe...")
    df = pd.DataFrame({occurrences_column: fd, users_column: users_occurrences})
    print("Done")
    return df


def generate_matrices(num_files=5):
    df = pd.DataFrame()
    for province in ["buenosaires", "larioja", "tucuman"]:
        jsons = os.path.join("data/tweets", province, "*.json")

        jsons = glob.glob(jsons)[:4]

        province_df = get_province_df(province, jsons)

        df = df.add(province_df, fill_value=.0)


    df.to_csv("matrix.csv")

if __name__ == '__main__':
    fire.Fire(generate_matrices)
