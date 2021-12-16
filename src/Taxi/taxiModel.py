
from src.Utils.database import Database
# Imports ObjectId to convert to the correct format before querying in the db
from bson.objectid import ObjectId
from src.Utils.CollectionMap import CollectionMapper

# Taxi document contains reg no (String), brand (String), model (String), type (String) and currentLocation (GeoJSON)fields
class TaxiModel:
    TAXI_COLLECTION = 'taxi_location'

    def __init__(self):
        self._db = Database()
        self._latest_error = ''

    def __get_taxi_collection (self, city):
        self._db_collection = CollectionMapper(city)
        self._city_db = self._db_collection.get_collection_name
        return self._city_db

    # Latest error is used to store the error string in case an issue. It's reset at the beginning of a new function call
    @property
    def latest_error(self):
        return self._latest_error

    # Since taxi reg no should be unique in taxis collection, this provides a way to fetch the taxi document based on the taxi reg no
    def find_taxi_by_reg_no(self,city, reg_no):
        collection = self.__get_taxi_collection(city)
        print("querying for taxi - "+reg_no)
        key = {'taxi_reg_no': reg_no}
        return self.__find(collection, key)

    # Finds a document based on the unique auto-generated MongoDB object id
    def find_by_object_id(self, city, obj_id):
        collection = self.__get_taxi_collection(city)
        key = {'_id': ObjectId(obj_id)}
        return self.__find(collection, key)

    # Private function (starting with __) to be used as the base for all find functions
    def __find(self, collection, key):
        taxi_document = self._db.get_single_data(collection, key)
        return taxi_document

    # This first checks if a taxi already exists with that reg no. If it does, it populates latest_error and returns -1
    # If a taxi doesn't already exist, it'll insert a new document and return the same to the caller

    def insertNewTaxi(self, reg_no, brand, model, type, base_rate,  vacant, lat,long, city):
        self._latest_error = ''
        print("Inserting data for New Taxi with reg_no - "+reg_no+" to Taxis Collection....")
        taxis_document = self.find_taxi_by_reg_no(city,reg_no)

        if (taxis_document != None):
            print(f'Taxi with Regd No-  {reg_no} already exists')
            return -1

        currentCoordinates = {'type': "Point", 'coordinates': [long, lat]}
        taxi_data = {'taxi_reg_no': reg_no, 'brand': brand, 'model': model, 'taxi_type': type, 'base_rate': base_rate,
                     'vacant': vacant, 'location': currentCoordinates, 'location_name':city}

        collection = self.__get_taxi_collection(city)

        taxi_obj_id = self._db.insert_single_data(collection, taxi_data)

        print(f'Inserted the taxi to the {collection} collection')
        return #self.find_by_object_id(collection, taxi_obj_id)

    # Find taxis by proximity and taxi type but limit the number of search results returned to the user
    def find_by_proximity(self, geospacial_location, proximity, search_limit, taxi_type ='All'):
        collection = self.__get_taxi_collection(geospacial_location['city'])
        if taxi_type != 'All':
            key = {'$and': [{'location':
                   {'$geoWithin':
                        {'$centerSphere': [geospacial_location['coordinates'], proximity / 6371]}}}
                            ,{'taxi_type': taxi_type}
                            ,{'vacant':'vacant'}
                            ]}
        else:
            key = {'$and': [{'location':
                   {'$geoWithin':
                        {'$centerSphere': [geospacial_location['coordinates'], proximity / 6371]}}}
                            ,{'vacant':'vacant'}
                            ]}

        return self._db.get_multiple_data(collection, key, search_limit)

    def upsertTaxiCoords(self,reg_no,lat,long, city):
        print("Upserting Taxi Coords")
        collection = self.__get_taxi_collection(city)
        filter = {'taxi_reg_no':reg_no}
        currentCoordinates = {'type': "Point", 'coordinates': [long, lat]}
        record = {'taxi_reg_no': reg_no, 'currentCoordinates': currentCoordinates}
        self._db.upsertData(collection,filter,record)

        # Find taxis by proximity and taxi type but limit the number of search results returned to the user

    def get_taxi_details(self, reg_no, city):
        collection = self.__get_taxi_collection(city)
        key = {'taxi_reg_no': reg_no}
        return self._db.get_single_data(collection, key)


    def update_one(self, city, taxi_reg_no, taxi_coord, user_coord ,status):
        collection = self.__get_taxi_collection(city)
        search_key = {'taxi_reg_no': taxi_reg_no}
        update_key = {'vacant': status}
        return self._db.upsertData(collection, search_key, update_key, False)

    '''
    def update_one(self, reg_no, status, city):
        collection = self.__get_taxi_collection(city)
        search_key = {'taxi_reg_no': reg_no}
        update_key = {"$set": {'status': status}}
        return self._db.upsertData(collection, search_key, update_key)
    '''