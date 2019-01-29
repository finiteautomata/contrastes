"""Create users"""

import pymongo
import fire
import json
import glob
import os
from pymongo.errors import DuplicateKeyError


def create_texts(database_name="contrastes"):
    client = pymongo.MongoClient('localhost')
    db = client[database_name]
    
    
    print("-- Cantidad de usuarios: {}".format(db.users.count()))
    print("-- Hay {} usuarios sin texto".format(db.users.find({
        "text": {"$exists": False}
    }).count()))
    
    
    for i, user in enumerate(db.users.find({"text": {"$exists": False}})):
        tweets = db.tweets.find({"user_id": user["id"]}, {"text": 1, "_id": 0})
        
        text = "\n".join(tweet["text"] for tweet in tweets)
        
        db.users.update_one(
            {"id": user["id"]},
            {"$set": {"text": text} }
        )
        if i % 500 == 0:
            print("{:.1f}K usuarios procesados".format(i/1000))
            
if __name__ == '__main__':
    fire.Fire(create_texts)
