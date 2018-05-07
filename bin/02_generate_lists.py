"""Generate lists of candidate words.

Note: see https://github.com/daleman/tesis/blob/master/notebooks/info.ipynb
"""

import fire
import numpy as np
from scipy.stats import entropy
from contrastes import read_occurrence_dataframe

def calculate_information_value(df, occurrence_column, columns):
    entr = df[columns].apply(entropy, axis=1, raw=True)
    delta = np.log(23) - entr

    log_occ = np.log(df[occurrence_column])
    norm_p = log_occ / log_occ.max()

    return norm_p * delta



def generate_lists(
    input_path="output/provinces_words.csv",
):
    """
    Generate ordered lists for each metric words and users

    Params:
    -------
    input_path: string (default="output/provinces_words.csv")
        Path to word-provinces matrix
    """
    df = read_occurrence_dataframe(input_path, filter_words=True)

    df["ival_palabras"] = calculate_information_value(df, "cant_palabra", df.cant_palabras)
    df["ival_personas"] = calculate_information_value(df, "cant_usuarios", df.cant_personas)
    df["ival"] = df["ival_palabras"] * df["ival_personas"]


    columns = [
        "cant_palabra",
        "cant_usuarios",
        "posicion",
    ]

    lists = {
        "personas": df.sort_values("ival_personas", ascending=False),
        "palabras": df.sort_values("ival_palabras", ascending=False),
        "palabras_personas" : df.sort_values("ival", ascending=False)

    }

    for k, df_sorted in lists.items():
        output_path = "output/listado_{}.csv".format(k)
        df_sorted["posicion"] = range(1, len(df)+1)

        df_sorted.to_csv(
            output_path,
            columns=columns,
            index_label="palabra",
        )

if __name__ == '__main__':
    fire.Fire(generate_lists)
