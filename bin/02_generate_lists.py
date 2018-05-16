"""Generate lists of candidate words.

Note: see https://github.com/daleman/tesis/blob/master/notebooks/info.ipynb
"""

import fire
import os
from contrastes import read_occurrence_dataframe
from contrastes.information_value import information_value
from contrastes.geo import region, places

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



def save_lists(lists, columns, output_path):
    """
    Save lists.

    Arguments:
    ---------

    lists: dict of (str, pandas.DataFrame)

        Map from list name to proper list.

    columns: list of strings
        Columns to save in 'shortened mode'
    """


    for k, df_sorted in lists.items():
        """
        Saving two kind of lists: one with just a few columns, and other complete

        This is in order to "debug" if there is any kind of problem...
        """
        for limit in [1000, 5000]:
            output_file = os.path.join(
                output_path,
                "listado_{}_{}.csv".format(k, limit)
            )

            output_complete_file = os.path.join(
                output_path,
                "listado_{}_{}_completo.csv".format(k, limit)
            )

            print("Generating {}".format(output_file))
            df_sorted[:limit].to_csv(
                output_file,
                index_label="palabra",
                columns=columns
            )

            print("Generating {}".format(output_complete_file))

            df_sorted[:limit].to_csv(
                output_complete_file,
                index_label="palabra",
                columns=columns + list(df_sorted.columns.difference(columns))
            )




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

    lists = {
        "personas": df.sort_values("ival_personas", ascending=False).copy(),
        "palabras": df.sort_values("ival_palabras", ascending=False).copy(),
        "palabras_personas": df.sort_values("ival", ascending=False).copy()
    }


    save_lists(
        lists,
        columns = [
            "cant_palabra",
            "cant_usuarios",
            "posicion",
            "region",
            "es_lugar",
        ],
        output_path=output_path
    )


if __name__ == '__main__':
    fire.Fire(generate_lists)
