import pymongo
# Define a global MongoClient instance
_mongo_client = None
from typing import Literal, Optional

def get_mongo_client():
    """Creates or retrieves the global MongoDB client instance."""
    global _mongo_client
    if _mongo_client is None:
        _mongo_client = pymongo.MongoClient("mongodb+srv://alham0046:alham789@cluster0.odsdwox.mongodb.net/")
        print("MongoDB connection initialized")
    return _mongo_client

databaseNameType = Literal['Hometheater']
collectionType = Literal['ShowsList', 'moviesList', None]

def mongoConnect(dbname: databaseNameType, collection:collectionType=None):
    """Connect to the specified database and collection, reusing the MongoClient."""
    client = get_mongo_client()  # Reuse the global client
    db = client[dbname]

    if not collection:
        return db
    else:
        # Check if the collection exists or create it
        if collection not in db.list_collection_names():
            return None
        return db[collection]