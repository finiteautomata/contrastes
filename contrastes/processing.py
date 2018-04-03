import re
from collections import defaultdict
from nltk.tokenize import TweetTokenizer
from nltk import FreqDist


tokenizer = TweetTokenizer(
    preserve_case=False,
    reduce_len=True,
    strip_handles=True
)

urls = r'(?:https?\://t.co/[\w]+)'


def tokenize(text, only_alpha=True, remove_hashtags=True):
    tokens = tokenizer.tokenize(text)

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
