"""Split ill-formed and heavy JSON into many smaller files."""
import fire
import os
import glob
import json

def get_chunks(path, chunk_size):
    with open(path) as f:
        while True:
            yield([json.loads(next(f)) for i in range(chunk_size)])


def split_tweet_files(path, chunk_size=50000):
    """Split ill-formed and heavy JSON

    Arguments
    --------

    path: string
        Where to find jsons
    """

    json_paths = glob.glob(os.path.join("{}", "*.json").format(path))

    for json_path in json_paths:
        _, base = os.path.split(json_path)
        province_name = base.split("_")[0]

        newdir = os.path.join(path, province_name)

        try:
            os.makedirs(newdir)
        except OSError as e:
            print("Directory already created:{}".format(newdir))

        print("Splitting {} with chunk_size = {}".format(json_path, chunk_size))
        for i, chunk in enumerate(get_chunks(json_path, 50000)):
            num_file = str(i+1).zfill(3)
            newfile = os.path.join(newdir, "{}.json".format(num_file))
            json.dump(chunk, open(newfile, "w"))
            print(newfile)


        print(json_path)

if __name__ == '__main__':
    fire.Fire(split_tweet_files)
