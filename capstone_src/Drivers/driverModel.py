
from src.Utils.database import Database
# Imports ObjectId to convert to the correct format before querying in the db
from bson.objectid import ObjectId

class DriverModel:
    DRIVER_COLLECTION = 'drivers'

    def __init__(self):
        self._db = Database()
        self._latest_error = ''

    # Latest error is used to store the error string in case an issue. It's reset at the beginning of a new function call
    @property
    def latest_error(self):
        return self._latest_error

    # Since Drivername should be unique in drivers collection, this provides a way to fetch the driver document based on the drivername
    def find_by_drivername(self, driver):
        key = {'drivername': driver}
        driver_doc = self.__find(key)
        if driver_doc == None:
            self._latest_error = f'Driver {driver} does not exist in Driver collection'
            return -1
        else:
            return driver_doc

    # Finds a document based on the unique auto-generated MongoDB object id
    def find_by_object_id(self, obj_id):
        key = {'_id': ObjectId(obj_id)}
        return self.__find(key)

    # Private function (starting with __) to be used as the base for all find functions
    def __find(self, key):
        driver_document = self._db.get_single_data(DriverModel.DRIVER_COLLECTION, key)
        return driver_document

    # Private function to get the exact value for a given key in a single document
    def __findkey(self, filters, key):
        driver_document = self._db.get_single_data_with_filter(DriverModel.DRIVER_COLLECTION, filters, key)
        return driver_document

    # This first checks if a driver already exists with that name. If it does, it populates latest_error and returns -1
    # If a driver doesn't already exist, it'll insert a new document and return the same to the caller
    def insertNewDriver(self, drivername, email, joinedDate, gender, phoneNo, city, currentLat, currentLong):
        self._latest_error = ''
        print("Adding new Driver - "+drivername)
        driver_document = self.find_by_drivername(drivername)
        if driver_document != -1:
            self._latest_error = f'Driver {drivername} already exists'
            return -1
        currentCoordinates = {'type': "Point", 'coordinates': [currentLat, currentLong]}
        driver_data = {
            'drivername': drivername,
            'email': email,
            'joinedDate': joinedDate,
            'gender': gender,
            'phoneNo': phoneNo,
            'city': city,
            'currentCoordinates': currentCoordinates
        }
        driver_obj_id = self._db.insert_single_data(DriverModel.DRIVER_COLLECTION, driver_data)
        return self.find_by_object_id(driver_obj_id)

