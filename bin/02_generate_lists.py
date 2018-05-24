"""Generate lists of candidate words.

Note: see https://github.com/daleman/tesis/blob/master/notebooks/info.ipynb
"""

import fire
import os
from contrastes import read_occurrence_dataframe
from contrastes.lists import add_info


def save_lists(df, output_path):
    """
    Save lists.

    Arguments:
    ---------

    df: pandas.DataFrame
        Occurrence dataframe, with added info
    """

    word_list = df[(df.rank_palabras <= 1000) |\
                   (df.rank_personas <= 1000) |\
                   (df.rank_palper <= 1000)]

    not_labeled = word_list[word_list.etiqueta.isna()].copy()

    # Add extra info
    not_labeled["lugar"] = not_labeled.es_lugar.apply(
        lambda w: "lugar" if w else "ok"
    )
    not_labeled["provincias_sin_esa_palabra"] = 23 - not_labeled.cant_provincias

    columns=["region", "lugar", "provincias_sin_esa_palabra"]

    print("Lists of first 1000 words")
    print("Number of total words (without repetition): {}".format(len(word_list)))
    print("Not labeled:{} palabras".format(not_labeled.shape[0]))
    print("Those of which {} are places".format(sum(not_labeled.es_lugar)))

    complete_path = os.path.join(output_path, "1000_no_etiquetadas_completo.csv")
    reduced_path = os.path.join(output_path, "1000_no_etiquetadas_random_reducido.csv")

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
