import re
import itertools
import json
import multiprocessing
import pandas as pd
from contextlib import closing
from collections import defaultdict
from nltk.tokenize import TweetTokenizer
from nltk import FreqDist


_tokenizer = TweetTokenizer(
    preserve_case=False,
    reduce_len=True,
    strip_handles=True
)

urls = r'(?:https?\://t.co/[\w]+)'


def tokenize(text, only_alpha=True, remove_hashtags=True):
    tokens = _tokenizer.tokenize(text)

    if only_alpha:
        tokens = [tk for tk in tokens if tk.isalpha()]
    else:
        if remove_hashtags:
            tokens = [tk for tk in tokens if tk[0] != "#"]
        tokens = [tk for tk in tokens if not re.match(urls, tk)]
    return tokens


def get_counters(tweets):
    """
    Returns a pair (fd, users) for a collection of tweets

    Parameters
    ----------
    tweets: List of dicts

    Returns:
    -------

    A pair (fd, users) where

    fd: nltk.FreqDist
        Occurrences of tokens

    users: defaultdict(set) of tokens -> users
        Dictionary containing users of given tokens
    """
    fd = FreqDist()
    users = defaultdict(set)

    for tweet in tweets:
        text = tweet['text']
        tokens = tokenize(text)
        for token in tokens:
            fd[token] += 1
            users[token].add(tweet['user']['id'])
    return fd, users

def merge_counters(fds, user_counters):
    """
    Takes as input the output of get_counters for multiple files and merge them

    Parameters:
    ----------

    fds: list of nltk.FreqDist

    user_counters: list of defaultdict(set)
        Dictionaries containing users of given tokens

    """
    fd = FreqDist()
    users = None

    for (other_fd, users_freq) in zip(fds, user_counters):
        fd += other_fd
        if users is None:
            users = users_freq
        else:
            # Tengo que mergear los dicts de aquellas existentes
            for k in itertools.chain(users.keys(), users_freq.keys()):
                users[k] = users[k].union(users_freq[k])

    return fd, users


def _get_counters_from_file(json_path):
    return get_counters(json.load(open(json_path)))


def build_province_df(province_name, jsons, no_workers=4):
    """
    Creates dataframe for a Province
    """
    with closing(multiprocessing.Pool(no_workers, maxtasksperchild=1)) as pool:
        fds, user_counters = zip(*pool.map(_get_counters_from_file, jsons))
    fd, users = merge_counters(fds, user_counters)

    users_occurrences = {k:len(v) for k, v in users.items()}

    occurrences_column = "{}_ocurrencias".format(province_name)
    users_column = "{}_usuarios".format(province_name)

    df = pd.DataFrame({
        occurrences_column: fd,
        users_column: users_occurrences
    })

    return df


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

        df = df[(df.cant_palabra >= min_words) &\
                (df.cant_usuarios >= min_users) ]

    df.cant_palabras = cant_palabras
    df.cant_personas = cant_personas

    return df

def build_dataframe_from_users(users):
    """
    Build dataframe from users.

    Arguments:
    ---------


    """

    def get_bow(user):
        bow = {}

        tokens = tokenize(user["text"])
        for token in tokens:
            bow[token] = bow.get(token, 0) + 1
        return bow

    columns = {}

    for user in users:
        bow = get_bow(user)
        province = user["provincia"]

        occ_column = province + "_ocurrencias"
        user_column = province + "_usuarios"

        if occ_column not in columns:
            columns[occ_column] = {}
            columns[user_column] = {}

        for tok, count in bow.items():
            columns[occ_column][tok] = columns[occ_column].get(tok, 0) + count
            columns[user_column][tok] = columns[user_column].get(tok, 0) + 1


    df = pd.DataFrame.from_dict(columns)

    df.fillna(0, inplace=True)
    df.fillna(0, inplace=True)
    return df
