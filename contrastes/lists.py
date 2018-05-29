import os
import pandas as pd
from .information_value import information_value
from .geo import places, region

def get_label():
    """
    Get pd.Series of labeled data.
    """
    labeled_df = pd.read_csv("data/listado_definitivo.csv", index_col=0)
    label = labeled_df["Palabra Candidata"].copy()
    label[label == "0,5"] = "0.5"
    return label.astype("float")


def _add_fnorm(df):
    fnorm_cols = []
    for col in df.cant_palabras:
        total_sum = df[col].sum()
        prov = col.split("_")[0]

        fnorm_col = "fnorm_{}".format(prov)
        fnorm_cols.append(fnorm_col)

        df[fnorm_col] = df[col] * (1000000.0 / total_sum)

    df["fnorm_max"] = df[fnorm_cols].max(axis=1)
    df["prov_max"] = df[fnorm_cols].idxmax(axis=1)
    df["prov_max"] = df["prov_max"].apply(lambda w: w.split("_")[1])
    # This is the minimum of nonzero columns
    df["fnorm_min"] = df[fnorm_cols][df > 0].min(axis=1)
    df["prov_min"] = df[fnorm_cols][df > 0].idxmin(axis=1)
    df["prov_min"] = df["prov_min"].apply(lambda w: w.split("_")[1])

    df["max_dif"] = df["fnorm_max"] / df["fnorm_min"]



def _add_ival(df):
    df["ival_palabras"] = information_value(df, "cant_palabra",
                                            df.cant_palabras)
    df["ival_personas"] = information_value(df, "cant_usuarios",
                                            df.cant_personas)
    df["ival_palper"] = df["ival_palabras"] * df["ival_personas"]

    df["rank_palabras"] = df["ival_palabras"].rank(ascending=False)
    df["rank_personas"] = df["ival_personas"].rank(ascending=False)
    df["rank_palper"] = df["ival_palper"].rank(ascending=False)


def add_info(df):
    """
    Add information value and other stuff
    """
    print("Calculating entropy, regions, and stuff...")
    _add_ival(df)

    df["region"] = df[df.cant_personas].apply(region, axis=1)

    lugares = places()
    df["es_lugar"] = df.index.map(lambda w: w in lugares)
    df["etiqueta"] = get_label()
    _add_fnorm(df)
    df["provincias_sin_esa_palabra"] = 23 - df["cant_provincias"]


def save_unlabeled_list(df, output_path, threshold=1000):
    """
    Save list of unlabeled words.

    Arguments:
    ---------

    df: pandas.DataFrame
        Occurrence dataframe, with added info
    """

    word_list = df[(df.rank_palabras <= threshold) |
                   (df.rank_personas <= threshold) |
                   (df.rank_palper <= threshold)]

    not_labeled = word_list[word_list.etiqueta.isna()].copy()

    # Add extra info
    not_labeled["lugar"] = not_labeled.es_lugar.apply(
        lambda w: "lugar" if w else "ok"
    )

    columns = ["region", "lugar", "provincias_sin_esa_palabra"]

    print("Lists of first {} words".format(threshold))
    print(
        "Number of total words (without repetition): {}".format(len(word_list))
    )
    print("Not labeled:{} palabras".format(not_labeled.shape[0]))
    print("Those of which {} are places".format(sum(not_labeled.es_lugar)))

    complete_path = os.path.join(output_path,
                                 "1000_no_etiquetadas_completo.csv")
    reduced_path = os.path.join(output_path,
                                "1000_no_etiquetadas_random_reducido.csv")

    reordered_columns = columns + list(not_labeled.columns.difference(columns))

    not_labeled.to_csv(complete_path,
                       columns=reordered_columns)
    print("Not labeled full list saved to {}".format(complete_path))
    # This shuffles the dataframe
    shuffled = not_labeled.sample(frac=1).copy()

    shuffled.to_csv(
        reduced_path,
        columns=columns
    )
    print("Not labeled shuffled reduced list saved to {}".format(reduced_path))


def save_info_by_provinces(df, output_path):
    print("Generating additional lists")

    def is_prov_fnorm(col):
        return "fnorm_" in col and "min" not in col and "max" not in col

    fnorm_cols = [col for col in df.columns if is_prov_fnorm(col)]
    assert(len(fnorm_cols) == 23)

    column_order = df.cant_palabras + ["cant_palabra"] +\
        df.cant_personas + ["cant_usuarios"] +\
        fnorm_cols + ["provincias_sin_esa_palabra"] +\
        ["fnorm_max", "prov_max", "fnorm_min", "prov_min", "max_dif"]

    extended_csv_path = os.path.join(
        output_path,
        "provincias_contraste_extendido.csv"
    )

    df.to_csv(extended_csv_path, columns=column_order)

    print("List saved to {}".format(extended_csv_path))

    resumed_order = [
        "fnorm_max", "prov_max", "fnorm_min", "prov_min", "max_dif",
        "provincias_sin_esa_palabra", "cant_usuarios"
    ]

    resumed_csv_path = os.path.join(
        output_path,
        "provincias_contraste_resumido.csv"
    )

    df.to_csv(resumed_csv_path, columns=resumed_order)

    print("Resumed list saved to {}".format(resumed_csv_path))
