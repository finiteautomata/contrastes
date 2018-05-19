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

def add_info(df):
    """
    Add information value and other stuff
    """
    print("Calculating entropy, regions, and stuff...")
    lugares = places()

    df["ival_palabras"] = information_value(df, "cant_palabra",
                                            df.cant_palabras)
    df["ival_personas"] = information_value(df, "cant_usuarios",
                                            df.cant_personas)
    df["ival"] = df["ival_palabras"] * df["ival_personas"]
    df["region"] = df[df.cant_personas].apply(region, axis=1)
    df["es_lugar"] = df.index.map(lambda w: w in lugares)
    df["etiqueta"] = get_label()
