"""This module implements Information-Gain Ratio.

This measure is described 
"""
from scipy.stats import entropy
import numpy as np

def igr(word_df, columns):
    data = word_df[columns]
    total_sum = data.sum()
    
    h_c = entropy(total_sum)
    
    word_sum = data.sum(axis=1)
    
    p_wi = word_sum / word_sum.sum()
    p_notwi = 1 -p_wi

    cond_entr_wi = data.apply(entropy, axis=1, raw=True)
    cond_entr_not_wi = (total_sum - data).apply(entropy, axis=1, raw=True)

    ig = h_c - (p_wi * cond_entr_wi + p_notwi * cond_entr_not_wi)
    iv = -p_wi * np.log(p_wi) - p_notwi * np.log(p_notwi)

    return ig / iv
    