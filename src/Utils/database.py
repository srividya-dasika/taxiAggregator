# Imports MongoClient for base level access to the local MongoDB
from pymongo import MongoClient


class Database:
    #HOST = '127.0.0.1'
    #PORT = '27017'
    DB_NAME = 'Taxi_Aggregator_DB'

    def __init__(self):
        #self._db_conn = MongoClient(f'mongodb://{Database.HOST}:{Database.PORT}')
        #self._db = self._db_conn[Database.DB_NAME]

        self._db_conn = MongoClient(
            "mongodb+srv://test:test@cluster0.5dwwl.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
        self._db = self._db_conn[Database.DB_NAME]

    # This method finds a single document using field information provided in the key parameter
    # It assumes that the key returns a unique document. It returns None if no document is found
    def get_single_data(self, collection, key):
        db_collection = self._db[collection]
        document = db_collection.find_one(key)
        return document

    def get_single_data_with_filter(self, collection, key, filter):
        db_collection = self._db[collection]
        document = db_collection.find_one(key , filter)
        return document

    # This method inserts the data in a new document. It assumes that any uniqueness check is done by the caller
    def insert_single_data(self, collection, data):
        db_collection = self._db[collection]
        document = db_collection.insert_one(data)
        return document.inserted_id

    def aggregate_data_daily(self, collection,pipeline ) :
        db_collection = self._db[collection]
        document= db_collection.aggregate(pipeline)
        return document

    def get_all_data(self,collection, key):
        db_collection = self._db[collection]
        documents = db_collection.find(key)
        return documents

    def insert_many(self, collection, obj):
        db_collection = self._db[collection]
        document = db_collection.insert_many(obj)
        return

    def delete_many(self, collection):
        db_collection = self._db[collection]
        document = db_collection.delete_many({})
        return

    # This method finds multple documents based on the key provided
    def get_multiple_data(self, collection, key):
        db_collection = self._db[collection]
        documents = db_collection.find(key)
        print("get mulitple data")
        return documents