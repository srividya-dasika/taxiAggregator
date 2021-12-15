from database import Database
# Imports ObjectId to convert to the correct format before querying in the db
from bson.objectid import ObjectId
from pymongo import GEOSPHERE
from bson.son import SON
from taxiModel import Taxi


# User document contains details about the all registered Users/Riders of the TaxiApp
# Contains following fields Id (AutoPopulated), Name (String), Email (String), Gender (String),  and role (String) fields
class UserModel:
    USER_COLLECTION = 'users'

    def __init__(self):
        self._db = Database()
        self._latest_error = ''

    # Latest error is used to store the error string in case an issue. It's reset at the beginning of a new function call
    @property
    def latest_error(self):
        return self._latest_error

    # Since username should be unique in users collection, this provides a way to fetch the user document based on the username
    def find_by_username(self, username):
        key = {'username': username}
        user_doc = self.__find(key)
        if user_doc == None:
            self._latest_error = f'User {username} does not exist in User collection'
            return -1
        else:
            return user_doc

    # Finds a document based on the unique auto-generated MongoDB object id
    def find_by_object_id(self, obj_id):
        key = {'_id': ObjectId(obj_id)}
        return self.__find(key)

    # Private function (starting with __) to be used as the base for all find functions
    def __find(self, key):
        user_document = self._db.get_single_data(UserModel.USER_COLLECTION, key)
        return user_document

    # Private function to get the exact value for a given key in a single document
    def __findkey(self, filters, key):
        user_document = self._db.get_single_data_with_filter(UserModel.USER_COLLECTION, filters, key)
        return user_document

    # This first checks if a user already exists with that username. If it does, it populates latest_error and returns -1
    # If a user doesn't already exist, it'll insert a new document and return the same to the caller
    def insertNewUser(self, username, email, joinedDate, gender, phoneNo, city, currentLat, currentLong):
        print("Inserting New User - "+username)
        self._latest_error = ''
        user_document = self.find_by_username(username)
        if user_document != -1:
            self._latest_error = f'Username {username} already exists'
            return -1

        currentCoordinates = {'type': "Point", 'coordinates': [currentLong, currentLat]}

        user_data = {
            'username': username,
            'email': email,
            'joinedDate': joinedDate,
            'gender': gender,
            'phoneNo': phoneNo,
            'city': city,
            'location': currentCoordinates
        }
        user_obj_id = self._db.insert_single_data(UserModel.USER_COLLECTION, user_data)
        return self.find_by_object_id(user_obj_id)

    def get_nearby_users(self,geospacial_location, proximity, search_limit):
            collection = self.USER_COLLECTION
            range_query = {'currentCoordinates': SON([("$near", geospacial_location), ("$maxDistance", proximity)])}
            return self._db.get_multiple_data(collection, range_query, search_limit)

class Users:
    def __init__(self, username,userLocation):
        self.username = username
        self.location = userLocation

    def login(self,username): #check if user exists in db and if so , login successfully
        return 1

    def add_new_user(self,username,location): #Adding new user into DB.
        return 1

    def requestTaxi(self,type):
        #  Send request to book a taxi to the taxi service.
        #  Wait till a taxi is allotted.
        #  Then change user status to riding
        print(self.username," requested for taxi...")
        taxis = Taxi()
        nearbyTaxis = taxis.getNearestTaxis(self.username,self.location,type)
#        if self.checkDriverAvailability(nearbyTaxis[0]):
 #           taxis.updateTaxiStatus(nearbyTaxis[0].reg_no,"Occupied")


    def checkDriverAvailability(self,Taxi):
        return True

