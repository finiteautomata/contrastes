#! coding: utf-8
"""Helpers para las notebooks de Information Value."""
import nltk
import json
import random

from scipy.stats import entropy
from nltk.corpus import stopwords, gutenberg
from numpy.random import multinomial
from nltk import word_tokenize



def shuffle(balls, bins):
    return multinomial(balls, [1. / bins] * bins)




def random_balls_in_bins(balls, bins):
    """Return a list of <bins> integers that sum <balls>.

    We can think this as a problem of bosons:

    We have to distribute balls in bins. To model this, we use a shuffle of

    'o' * balls + '|' * (bins-1)

    This results in a string of the form oo|ooo|oo where we leave the last '|' fixed

    Parameters:
    ----------

    balls: int > 0
        number of balls to distribute
    bins: int > 0
        number of bins

    Returns
    -------

    A list of <bins> integers that sum <balls>
    """
    balls_and_bins = list('o' * balls + '|' * (bins - 1))
    random.shuffle(balls_and_bins)

    bins = []
    current = 0

    for e in balls_and_bins:
        if e == 'o':
            current += 1
        elif e == '|':
            bins.append(current)
            current = 0

    bins.append(current)

    return bins


def simulated_shuffled_entropy(n, p):
    """Calculate simulated-shuffled entropy.

    Parameters
    ----------

    n: int
        Number of occurrences of word
    p: int
        Number of parts in text
    """
    shuffled_words = random_balls_in_bins(balls=n, bins=p)
    assert(sum(shuffled_words) == n)
    return entropy(shuffled_words)


def simulated_shuffled_entropy_multinomial(n, p):
    """Calculate simulated-shuffled entropy.

    Parameters
    ----------

    n: int
        Number of occurrences of word
    p: int
        Number of parts in text
    """
    shuffled_words = shuffle(balls=n, bins=p)
    assert(sum(shuffled_words) == n)
    return entropy(shuffled_words)
