"""Split ill-formed and heavy JSON into many smaller files."""
import fire
import os
import glob
import json
import nltk
import pandas as pd
from contrastes.processing import build_province_df

def get_provinces(tweets_path):
    subdirs = glob.glob(os.path.join(tweets_path, "**/"))
    provinces = [os.path.basename(os.path.normpath(p)) for p in subdirs]

    return provinces

def generate_matrix(
    output_path="output/provinces_words.csv",
    tweets_path="data/tweets",
    num_files=None
):
    """
    Generate occurrence matrix for both words and users

    Params:
    -------
    tweets_path: string (default="data/tweets")
        Path where to find tweets for each province.
        Tweets will be found in each subfolder of the given path.

    output_path: string (default="output/provinces_words.csv")
        Path where to write the generated csv

    num_files: int (default = None)
        How many tweet files should we use? (just for debugging purposes)
    """
    df = pd.DataFrame()
    provinces = get_provinces(tweets_path)
    path_template = os.path.join(tweets_path, "{}", "*.json")

    for province in provinces:

        json_paths = glob.glob(path_template.format(province))
        if num_files:
            json_paths = json_paths[:num_files]

        print("Processing {}, {} files ...".format(province, len(json_paths)),
              end="")
        province_df = build_province_df(province, json_paths)
        df = df.add(province_df, fill_value=0)
        print("done")

    df = df.fillna(0).astype("int64")
    df.to_csv(output_path, index_label="palabra")


if __name__ == '__main__':
    fire.Fire(generate_matrix)
