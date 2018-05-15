"""Geographical functions for words."""
import nltk
import json


def region(word_series, threshold=0.95):
    """Given a pandas series representing a word, return the region the word is used more in.

    Parameters:
    -----------

    word_series: pandas.Series
        A series of columns province1_count, province2_count, etc.

    threshold: float number between 0 and 1, default 0.95
        Threshold to select provinces.

    Returns:
    --------

        list of provinces, which sum up at least threshold frequency of use.
    """
    ws = word_series / word_series.sum()
    accum = 0
    provs = []

    for prov in ws.sort_values(ascending=False).index:
        accum+= ws[prov]
        provs.append(prov)
        if accum >= threshold:
            break

    return [p.split("_")[0] for p in provs]


def places():
    with open('data/localidades/cabeceras.geojson') as cab,\
         open('data/localidades/capitales.geojson') as cap,\
         open('data/localidades/localidades.geojson') as loc,\
         open('data/localidades/departamentos.geojson') as dep:
        cabeceras = json.load(cab)
        capitales = json.load(cap)
        localidades = json.load(loc)
        departamentos = json.load(dep)
        lugares = set([])
        for a in [cabeceras, capitales, localidades, departamentos]:
            for n in a['features']:
                for w in nltk.word_tokenize(n['properties']['nombre']):
                    lugares.add(w.lower())

    return lugares