# Imports MongoClient for base level access to the local MongoDB
from pymongo import MongoClient, GEOSPHERE


class Database:
    HOST = '3.92.193.183'
    PORT = '27017'
    DB_NAME = 'TaxiApp_DB'

    def __init__(self):
       # uri = "mongodb://user:password@example.com/?authSource=the_database&authMechanism=SCRAM-SHA-1"

        #self._db_conn = MongoClient(f'mongodb://taxiAppUser:Test1234@{Database.HOST}:{Database.PORT}/?authSource={Database.DB_NAME}&authMechanism=SCRAM-SHA-1')
        #self._db = self._db_conn[Database.DB_NAME]


        self._db_conn = MongoClient("mongodb+srv://test:test@cluster0.5dwwl.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
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

    def updateOne(self,collection, filter, update,upsert= False):
        db_collection = self._db[collection]
        return db_collection.update_one(filter, update)

    def upsertData(self,collection,filter,record):
        db_collection = self._db[collection]
        documents = db_collection.replace_one(filter,record,upsert=False)

    def insert_many(self, collection, obj):
        db_collection = self._db[collection]
        document = db_collection.insert_many(obj)
        return

    def delete_many(self, collection):
        db_collection = self._db[collection]
        document = db_collection.delete_many({})
        return

    # This method finds multple documents based on the key provided

    def get_multiple_data(self, collection, key, search_limit):
        db_collection = self._db[collection]
        print(f'creating index on {collection}')
        db_collection.create_index([('currentCoordinates', GEOSPHERE)])
        print(f'querying for {key} with limit {search_limit}')
        records = db_collection.find(key).limit(search_limit)
        i=0
        for record in records:
            i=i+1
        print(f'Count of records received = {i}')
        return db_collection.find(key).limit(search_limit)

