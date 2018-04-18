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
    """
    Return a list of <bins> integers that sum <balls>.
    We can think this as a problem of bosons:


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

    probabilities = [1. / bins] * bins
    return multinomial(balls, probabilities)




def simulated_shuffled_entropy(n, p):
    """Calculate simulated-shuffled entropy.

    Parameters
    ----------

    n: int
        Number of occurrences of word
    p: int
        Number of parts in text
    """
    shuffled_words = shuffle(balls=n, bins=p)
    return entropy(shuffled_words)
