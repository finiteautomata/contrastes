"""Generate lists of candidate words.

Note: see https://github.com/daleman/tesis/blob/master/notebooks/info.ipynb
"""

import fire
import os
from contrastes import read_occurrence_dataframe
from contrastes.lists import (
    add_info, save_unlabeled_list, save_info_by_provinces
)


def save_lists(df, output_path):
    save_unlabeled_list(df, output_path, threshold=1000)
    save_info_by_provinces(df, os.path.join(output_path, "complementarios/"))


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
