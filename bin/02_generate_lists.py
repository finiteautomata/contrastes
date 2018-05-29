"""Generate lists of candidate words.

Note: see https://github.com/daleman/tesis/blob/master/notebooks/info.ipynb
"""

import fire
import os
from contrastes import read_occurrence_dataframe
from contrastes.lists import add_info, save_unlabeled_list


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


def save_lists(df, output_path):
    save_unlabeled_list(df, output_path, threshold=1000)
    save_info_by_provinces(df, output_path)


def generate_lists(
    input_path="output/provinces_words.csv",
    output_path="output/listados/"
):
    """
    Generate ordered lists for each metric words and users

    Params:
    -------
    input_path: string (default="output/provinces_words.csv")
        Path to word-provinces matrix
    """
    print("Loading words from {}".format(input_path))

    df = read_occurrence_dataframe(input_path, filter_words=True)

    add_info(df)

    df.to_csv(os.path.join(output_path, "listado_completo.csv"))

    save_lists(
        df,
        output_path
    )

if __name__ == '__main__':
    fire.Fire(generate_lists)
