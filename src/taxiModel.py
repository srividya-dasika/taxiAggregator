from database import Database
# Imports ObjectId to convert to the correct format before querying in the db
from bson.objectid import ObjectId
from bson.son import SON
from pymongo import GEOSPHERE
from CollectionMap import CollectionMapper
from ServiceArea import ServiceArea
from Trip import Trip

# Taxi document contains reg no (String), brand (String), model (String), type (String) and currentLocation (GeoJSON)fields
class TaxiModel:
    TAXI_COLLECTION = 'taxi_location'

    def __init__(self):
        self._db = Database()
        self._latest_error = ''

    def __get_taxi_collection (self, city):
        print(f'[taxiModel]getting collection name for {city} ')
        self._db_collection = CollectionMapper(city)
        self._city_db = self._db_collection.get_collection_name
        print(f'{self._city_db}')
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
        print('__find', collection, key)
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
        print(f'getting collectionname for city - {geospacial_location}')
        collection = self.__get_taxi_collection(geospacial_location['city'])
        if taxi_type != 'All':
            key = {'$and': [{'currentCoordinates':
                   {'$geoWithin':
                        {'$centerSphere': [geospacial_location['coordinates'], proximity / 6371]}}}
                            ,{'taxi_type': taxi_type}
                            ,{'vacant':'vacant'}
                            ]}
        else:
            key = {'$and': [{'currentCoordinates':
                   {'$geoWithin':
                        {'$centerSphere': [geospacial_location['coordinates'], proximity / 6371]}}}
                            ,{'vacant':'vacant'}
                            ]}
        print(f'getting data from collection - {collection}')
        taxiData= self._db.get_multiple_data(collection, key, search_limit)
        print(f'Got Taxi Data from DB {taxiData}')
        docs = list(taxiData)
        taxi_dict = []
        print("Taxis data:", docs)
        for doc in docs:
           Dict = {'taxiName': doc['reg_no'], 'latitude': doc['currentCoordinates'].get('coordinates')[0],
                'longitude': doc['currentCoordinates'].get('coordinates')[1]}
           taxi_dict.append(Dict)
        return taxi_dict


    # Find taxis by proximity and taxi type but limit the number of search results returned to the user
    def getAllTaxisInArea(self,geospacial_location, proximity, search_limit):
        collection = self.__get_taxi_collection(geospacial_location['city'])
        range_query = {'currentCoordinates': SON([("$near", geospacial_location), ("$maxDistance", proximity)])}
        return self._db.get_multiple_data(collection, range_query, search_limit)

    def upsertTaxiCoords(self,reg_no,lat,long, city):
        print("Upserting Taxi Coords")
        collection = self.__get_taxi_collection(city)
        filter = {'taxi_reg_no':reg_no}
        currentCoordinates = {'type': "Point", 'coordinates': [long, lat]}
        record = {'taxi_reg_no': reg_no, 'currentCoordinates': currentCoordinates}
        self._db.upsertData(collection,filter,record)

    def get_taxi_details(self, reg_no, city):
        collection = self.__get_taxi_collection(city)
        key = {'taxi_reg_no': reg_no}
        return self._db.get_single_data(collection, key)

    # Find the taxi with that registration number and with that 'from_status' and update that to 'to_status'
    def update_booking(self, city, taxi_reg_no ,from_status, to_status):
        collection = self.__get_taxi_collection(city)
        print(f'updating the taxi {taxi_reg_no} status from {from_status} to {to_status}')
        search_key = {'reg_no': taxi_reg_no, 'vacant': from_status }
        update_key = {"$set": {'vacant': to_status}}
        status = self._db.updateOne(collection, search_key, update_key, False)
        print(f'Found taxi status count = {status.matched_count}')
        return status.matched_count


class Taxi:
    proximityRadius = 8  # assuming proximity factor as 3 kms.
    searchResultLimit = 5  # limit the number of search results

    def __init__(self, reg_no=0):
        self.reg_no = reg_no
        # self.location = location
        self.taxi_model = TaxiModel()

    def add_new_taxi(self, taxi_reg_no, location):  # Adding new user into DB.
        return 1

    def getNearestTaxis(self, username, userLocation, taxi_type):
        #  Send request to book a taxi to the taxi service.
        #  Wait till a taxi is allotted.
        #  Then change user status to riding
        print("Fetching taxis in", self.proximityRadius, "km radius for", username)
        obj_serv = ServiceArea()
        within_service_area = obj_serv.validate_service_area(userLocation)
        if within_service_area:
            # Mongoquery to get all nearby taxis.
            return self.taxi_model.find_by_proximity(userLocation, self.proximityRadius, self.searchResultLimit,
                                                     taxi_type)
        else:
            print('Error: Either city name is incorrect or user location is not in our service area')
            return -1

    def updateTaxiStatus(self, city, username, taxi_reg_no, from_status, to_status):
        ############## Send SNS to taxi
        ############## Send SNS to User
        status_count =  self.taxi_model.update_booking(city, taxi_reg_no, from_status, to_status)
        if status_count == 0: return -1
        else: return taxi_reg_no

    def startTrip(self, city, taxi_reg_no, customer_phone_no,taxi_current_coord,  taxi_dest_coord):
        self.trip_obj = Trip(city, taxi_reg_no, customer_phone_no)
        ############## Send SNS to taxi and user
        return self.trip_obj.start_trip(city, taxi_current_coord,  taxi_dest_coord)

    def endTrip(self, trip_id):
        return self.trip_obj.end_trip(trip_id)




