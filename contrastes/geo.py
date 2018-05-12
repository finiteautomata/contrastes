"""Geographical functions for words."""
def region(word_series, threshold=0.95):
    ws = word_series / word_series.sum()
    accum = 0
    provs = []

    for prov in ws.sort_values(ascending=False).index:
        accum+= ws[prov]
        provs.append(prov)
        if accum >= threshold:
            break

    return [p.split("_")[0] for p in provs]
