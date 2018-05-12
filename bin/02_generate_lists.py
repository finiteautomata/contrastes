"""Generate lists of candidate words.

Note: see https://github.com/daleman/tesis/blob/master/notebooks/info.ipynb
"""

import fire
from contrastes import read_occurrence_dataframe
from contrastes.information_value import information_value
from contrastes.geo import region

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

    print("Calculating entropy, regions, and stuff...")
    df["ival_palabras"] = information_value(df, "cant_palabra",
                                            df.cant_palabras)
    df["ival_personas"] = information_value(df, "cant_usuarios",
                                            df.cant_personas)
    df["ival"] = df["ival_palabras"] * df["ival_personas"]
    df["region"] = df[df.cant_personas].apply(region, axis=1)

    columns = [
        "cant_palabra",
        "cant_usuarios",
        "posicion",
    ]

    lists = {
        "personas": df.sort_values("ival_personas", ascending=False),
        "palabras": df.sort_values("ival_palabras", ascending=False),
        "palabras_personas": df.sort_values("ival", ascending=False)

    }

    for k, df_sorted in lists.items():
        output_path = "output/listado_{}.csv".format(k)
        df_sorted["posicion"] = range(1, len(df)+1)
        print("Generating {}".format(output_path))

        df_sorted.to_csv(
            output_path,
            index_label="palabra",
        )


if __name__ == '__main__':
    fire.Fire(generate_lists)
