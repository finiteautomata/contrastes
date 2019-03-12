import os
import pandas as pd
import re
from .information_value import information_value
from .geo import places, region
from . import argentina


def get_label():
    """
    Get pd.Series of labeled data.
    """
    labeled_df = pd.read_csv("data/listado_definitivo.csv", index_col=0)
    label = labeled_df["Palabra Candidata"].copy()
    label[label == "0,5"] = "0.5"
    return label.astype("float")


def _fnorm(df, col):
    total_sum = df[col].sum()
    return df[col] * (1000000.0 / total_sum)


def _add_fnorm(df):
    print("Adding fnorms...")
    fnorm_cols = []
    for col in df.columnas_palabras:
        prov = col.split("_")[0]

        fnorm_col = "fnorm_{}".format(prov)
        fnorm_cols.append(fnorm_col)

        df[fnorm_col] = _fnorm(df, col)

    df["fnorm_max"] = df[fnorm_cols].max(axis=1)
    df["prov_max"] = df[fnorm_cols].idxmax(axis=1)
    df["prov_max"] = df["prov_max"].apply(lambda w: w.split("_")[1])
    # This is the minimum of nonzero columns
    df["fnorm_min"] = df[fnorm_cols][df > 0].min(axis=1)
    df["prov_min"] = df[fnorm_cols][df > 0].idxmin(axis=1)
    df["prov_min"] = df["prov_min"].apply(lambda w: w.split("_")[1])

    df["max_dif"] = df["fnorm_max"] / df["fnorm_min"]


def _add_regional_info(df):
    """Add info for regions (Cuyo, Guaranitica, etc)."""
    fnorm_cols = []
    for region, provinces in argentina.regions.items():
        occ_cols = ["{}_ocurrencias".format(prov) for prov in provinces]
        user_cols = ["{}_usuarios".format(prov) for prov in provinces]

        occ_col = "{}_ocurrencias".format(region)
        fnorm_col = "fnorm_{}".format(region)
        fnorm_cols.append(fnorm_col)

        df[occ_col] = df[occ_cols].sum(axis=1)
        df[fnorm_col] = _fnorm(df, occ_col)
        df["{}_usuarios".format(region)] = df[user_cols].sum(axis=1)

    df["fnorm_region_max"] = df[fnorm_cols].max(axis=1)
    df["region_max"] = df[fnorm_cols].idxmax(axis=1)
    df["region_max"] = df["region_max"].apply(lambda w: w.split("_")[1])
    # This is the minimum of nonzero columns
    df["fnorm_region_min"] = df[fnorm_cols][df > 0].min(axis=1)
    df["region_min"] = df[fnorm_cols][df > 0].idxmin(axis=1)
    df["region_min"] = df["region_min"].apply(lambda w: w.split("_")[1])

    region_con_palabra = (df[fnorm_cols] > 0).sum(axis=1)
    df["region_sin_palabra"] = len(fnorm_cols) - region_con_palabra
    df["max_dif_region"] = df["fnorm_region_max"] / df["fnorm_region_min"]


def add_ival(df, normalize=False):
    print("Calculating information values...")
    df["ival_palabras"] = information_value(
        df, "cant_palabra", df.columnas_palabras, normalize=normalize
    )

    df["ival_personas"] = information_value(
        df, "cant_usuarios", df.columnas_personas, normalize=normalize
    )

    df["ival_palper"] = df["ival_palabras"] * df["ival_personas"]

    print("Calculating ranks...")
    df["rank_palabras"] = df["ival_palabras"].rank(ascending=False)
    df["rank_personas"] = df["ival_personas"].rank(ascending=False)
    df["rank_palper"] = df["ival_palper"].rank(ascending=False)


def add_info(df, normalize=False):
    """
    Add information value and other stuff
    """
    add_ival(df, normalize=normalize)

    no_provincias = len(df.columnas_palabras)

    df["provincias_sin_esa_palabra"] = no_provincias - df["cant_provincias"]
    df["region"] = df[df.columnas_personas].apply(region, axis=1)

    lugares = places()
    df["es_lugar"] = df.index.map(lambda w: w in lugares)
    df["etiqueta"] = get_label()
    _add_fnorm(df)
    _add_regional_info(df)


def save_list(df, columns, path, format='csv'):
    if format == 'csv':
        df.to_csv(path, columns=columns)
    elif format == 'xls':
        writer = pd.ExcelWriter(path, engine='xlsxwriter')
        df.to_excel(
            writer, columns=columns, encoding="ISO-8859-1",
            sheet_name='Sheet1')
        writer.close()
    print("List saved to {}".format(path))


def save_unlabeled_list(df, output_path, threshold=1000):
    """
    Save list of unlabeled words.

    Arguments:
    ---------

    df: pandas.DataFrame
        Occurrence dataframe, with added info
    """
    print("="*40)
    print("Saving lists to label\n\n")
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

    complete_path = os.path.join(
        output_path,
        "1000_no_etiquetadas_completo.csv"
    )
    reduced_path = os.path.join(
        output_path,
        "1000_no_etiquetadas_random_reducido.xls"
    )

    reordered_columns = columns + list(not_labeled.columns.difference(columns))

    print("**Not labeled complete list**")
    save_list(not_labeled, reordered_columns, complete_path)
    # This shuffles the dataframe
    shuffled = not_labeled.sample(frac=1).copy()
    print("**Not labeled and reduced shuffled list**")
    save_list(shuffled, columns, reduced_path, format="xls")


def save_info_by_provinces(df, output_path):
    print("=" * 40)
    print("Generating additional info by provinces\n\n")

    fnorm_cols = ["fnorm_{}".format(prov) for prov in argentina.provinces]
    assert(len(fnorm_cols) == 23)

    full_column_order = df.columnas_palabras + ["cant_palabra"] +\
        df.columnas_personas + ["cant_usuarios"] +\
        fnorm_cols + ["provincias_sin_esa_palabra"] +\
        ["fnorm_max", "prov_max", "fnorm_min", "prov_min", "max_dif"]

    extended_csv_path = os.path.join(
        output_path,
        "provincias_contraste_extendido.xls"
    )

    resumed_order = [
        "fnorm_max", "prov_max", "fnorm_min", "prov_min", "max_dif",
        "provincias_sin_esa_palabra", "cant_usuarios"
    ]

    resumed_csv_path = os.path.join(
        output_path,
        "provincias_contraste_resumido.xls"
    )


    print("** Provinces full list **")

    save_list(df, full_column_order, extended_csv_path, format="xls")

    print("** Provinces resumed list **")
    save_list(df, resumed_order, resumed_csv_path, format="xls")


def save_info_by_regions(df, output_path):
    print("=" * 40)
    print("Generating additional info by regions\n\n")

    regions = argentina.regions
    occ_cols = ["{}_ocurrencias".format(region) for region in regions]
    user_cols = ["{}_usuarios".format(region) for region in regions]
    fnorm_cols = ["fnorm_{}".format(region) for region in regions]

    assert(len(fnorm_cols) == 5)

    extended_columns = occ_cols + ["cant_palabra"] +\
        user_cols + ["cant_usuarios"] +\
        fnorm_cols + ["region_sin_palabra", "fnorm_region_max", "region_max",
                      "fnorm_region_min", "region_min", "max_dif_region"]

    extended_csv_path = os.path.join(
        output_path,
        "regiones_contraste_extendido.xls"
    )

    resumed_csv_path = os.path.join(
        output_path,
        "regiones_contraste_resumido.xls"
    )

    resumed_columns = [
        "fnorm_region_max", "fnorm_region_min",
        "region_max", "region_min",
        "cant_usuarios", "region_sin_palabra", "max_dif_region"
    ]

    print("** Regions extended list **")
    save_list(df, extended_columns, extended_csv_path, format="xls")
    print("** Regions resumed list **")
    save_list(df, resumed_columns, resumed_csv_path, format="xls")
