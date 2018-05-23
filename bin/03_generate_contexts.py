"""Generate lists of contexts.

"""

import pymongo
import glob
import random
import os
import json
import fire

database_name = "contrastes"


def serialize(tweet, provincia):
    ret = {k: tweet[k] for k in ["id", "text", "place"]}
    ret["provincia"] = provincia

    return ret


def save_tweets_to(path_to_tweets, collection, no_samples):
    directories = glob.glob(os.path.join(path_to_tweets, "**/"))

    print(directories)

    for path_to_province in directories:

        provincia = path_to_province.split("/")[-2]
        print("="*80)
        print(provincia)
        # Choose a sample of them
        files = glob.glob(os.path.join(path_to_province, "*.json"))
        files = random.sample(files, no_samples)

        print("Consuming files {}".format(files))

        for tweets_file in files:
            print(tweets_file)
            tweets = json.load(open(tweets_file))
            tweets = [serialize(tweet, provincia) for tweet in tweets]

            collection.insert_many(tweets)


def generate_contexts(path_to_tweets):
    """
    Generate tweet database.

    Parameters:
    -----------

    path_to_tweets: string
        Path to tweets. Should be separated in directories under the path.
    """

    client = pymongo.MongoClient('localhost', 27017)
    db = client[database_name]

    db.tweets.drop()
    db.tweets.create_index([('id', pymongo.ASCENDING)], unique=True)
    db.tweets.create_index(
        [('text', pymongo.TEXT)],
        default_language='spanish')

    save_tweets_to(path_to_tweets, db.tweets, 10)


if __name__ == '__main__':
    fire.Fire(generate_contexts)
