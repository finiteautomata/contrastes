"""Geographical functions for words."""
import nltk
import json
import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from multiprocessing import Pool
from .geo import mean_distance_score


_X_train = None
_X_test = None
_y_train = None
_y_test = None

_province_encoder = None

_default_clf_params = {
    "multi_class": 'multinomial', 
    "solver": 'saga', 
    "penalty": 'l2', 
    "max_iter": 250,
}

_clf_params = {}

def _fit_clf(num_words):
    print("Entrenando con {} palabras".format(num_words))
    X_tr = _X_train[:, :num_words]
    X_tst = _X_test[:, :num_words]
    
    clf = LogisticRegression(
        **_clf_params
    )
    clf.fit(X_tr, _y_train)

    acc = clf.score(X_tst, _y_test)
    md = mean_distance_score(clf, X_tst, _y_test, _province_encoder)
    
    print("{:<5} palabras ----> accuracy {:.2f} mean distance {}".format(
            num_words, acc*100, md
        ))
    return {"num_words": num_words, "clf": clf, "accuracy": acc, "mean_distance": md}
    

def fit_classifiers(X_train, y_train, X_test, y_test, province_encoder, range_num_words, clf_params={}, num_jobs=3):
    global _X_train, _X_test
    global _y_train, _y_test
    global _province_encoder
    global _clf_params
    
    _X_train = X_train
    _X_test = X_test
    _y_train = y_train
    _y_test = y_test
    _province_encoder = province_encoder
    
    _clf_params = _default_clf_params.copy()
    _clf_params.update(clf_params)
    
    print("Classifier params: {}".format(_clf_params))
    
    p = Pool(num_jobs)
    
    ret = p.map(_fit_clf, range_num_words)
    
    p.close()
    
    return ret
