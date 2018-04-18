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
