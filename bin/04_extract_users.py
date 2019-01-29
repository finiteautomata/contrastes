"""Create users"""

import pymongo
import fire
import json
import glob
import os
from pymongo.errors import DuplicateKeyError

def create_table(db, drop):
    if db.users.count() > 0:
        if drop:
            db.users.drop()
        else:
            print("Colección users ya existe -- saliendo")
            return
    db.users.create_index([('id', pymongo.ASCENDING)], unique=True)
    db.users.create_index([('provincia', pymongo.ASCENDING)], unique=False)
    
    print("Colección de usuarios creada")
    print("Índices:")
    
    for k, v, in db.users.index_information().items():
        print("{} ---> configuración {}".format(k, v))

def create_users_collection(path_to_tweets, database_name="contrastes", drop=False):
    client = pymongo.MongoClient('localhost')
    db = client[database_name]
    
    create_table(db, drop)
    
    """
    Vamos a sacar la info del campo user de los tweets que ya tenemos
    """
    directories = glob.glob(os.path.join(path_to_tweets, "**/"))
    print(directories)
    user_count = 0
    for path_to_province in directories:

        provincia = path_to_province.split("/")[-2]
        print("="*80)
        print(provincia)
        # Choose a sample of them
        files = glob.glob(os.path.join(path_to_province, "*.json"))

        current_user_id = None
        for tweets_file in files:
            tweets = json.load(open(tweets_file))
            
            for tweet in tweets:
                if current_user_id == tweet["user"]["id"]:
                    continue
                else:
                    current_user_id = tweet["user"]["id"]
                doc = tweet["user"]
                doc["provincia"] = provincia
                
                try:
                    db.users.insert_one(doc)
                    user_count += 1
                except DuplicateKeyError as e:
                    continue
        
                if user_count % 500 == 0:
                    print("{:.1f}K usuarios procesados".format(user_count / 1000))

    print("{} usuarios han sido creados ".format(db.users.count()))
if __name__ == '__main__':
    fire.Fire(create_users_collection)
