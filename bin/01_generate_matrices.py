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
from contrastes.processing import tokenize


def get_counters_from_file(json_path):
    """
    Returns a pair (fd, users) for a given collection of tweets

    Parameters
    ----------
    json_path: string
        Path to json, which should be a collection of tweets

    Returns:
    -------

    A pair (fd, users) where

    fd: nltk.FreqDist
        Occurrences of tokens

    users: defaultdict(set) of tokens -> users
        Dictionary containing users of given tokens
    """
    print("file {}".format(json_path))
    tweets = json.load(open(json_path))
    fd = nltk.FreqDist()
    users = defaultdict(set)

    for tweet in tweets:
        text = tweet['text']
        tokens = tokenize(text)
        for token in tokens:
            fd[token] += 1
            users[token].add(tweet['user']['id'])
    return fd, users


def get_province_df(province_name, jsons, no_workers=4):
    """
    Creates dataframe for a Province
    """
    print("Processing {}".format(province_name))
    pool = multiprocessing.Pool(no_workers, maxtasksperchild=1)

    fds = pool.map(get_counters_from_file, jsons)

    fd = nltk.FreqDist()
    users = None

    for (other_fd, users_freq) in fds:
        fd += other_fd
        if users is None:
            users = users_freq
        else:
            # Tengo que mergear los dicts de aquellas existentes
            for k in itertools.chain(users.keys(), users_freq.keys()):
                users[k] = users[k].union(users_freq[k])

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

        jsons = glob.glob(jsons)[:5]

        province_df = get_province_df(province, jsons)

        df = df.add(province_df, fill_value=.0)


    df.to_csv("matrix.csv")

if __name__ == '__main__':
    fire.Fire(generate_matrices)
