# Imports MongoClient for base level access to the local MongoDB
from pymongo import MongoClient, GEOSPHERE
# Imports datetime class to create timestamp for weather data storage


# Database host ip and port information

HOST = '54.234.37.90'
PORT = '27017'

RELATIVE_CONFIG_PATH = '../config/'

DB_NAME = 'TaxiApp_DB'
USER_COLLECTION = 'users'
DRIVER_COLLECTION = 'drivers'
TAXI_COLLECTION = 'taxis'
LOCATION_COLLECTION = 'device_access'
# This will initiate connection to the mongodb
#db_handle = MongoClient(f'mongodb://{HOST}:{PORT}')
db_handle = MongoClient(f'mongodb://taxiAppUser:Test1234@{HOST}:{PORT}/?authSource={DB_NAME}&authMechanism=SCRAM-SHA-1')
# We drop the existing database including all the collections and data
#db_handle.drop_database(DB_NAME)

# We recreate the database with the same name
taxi_dbh = db_handle[DB_NAME]


# user data import
# User document contains username (String), email (String), and role (String) fields
# Reads users.csv one line at a time, splits them into the data fields and inserts

# This creates and return a pointer to the users collection
user_collection = taxi_dbh[USER_COLLECTION]
user_collection.delete_many({})
with open(RELATIVE_CONFIG_PATH+USER_COLLECTION+'.csv', 'r') as user_fh:
    for user_row in user_fh:
        user_row = user_row.rstrip()
        if user_row:
            (username, email, joinedDate, gender, phoneNo, city,onTrip, currentLong, currentLat) = user_row.split(',')
        currentCoordinates = {'type': "Point",'coordinates': [float(currentLong), float(currentLat)]}
        user_data = {
                        'username': username,
                        'email': email,
                        'joinedDate': joinedDate,
                        'gender':gender,
                        'phoneNo':phoneNo,
                        'city':city,
                        'onTrip':onTrip,
                        'currentCoordinates':currentCoordinates
                    }
        print(f'{user_data}')
        # This inserts the data item as a document in the user collection
        user_collection.insert_one(user_data)


## Driver document contains Driver name (String), current_cab_id (String), joinedDate (String)
## Reads driver.csv one line at a time, splits them into the data fields and inserts
'''
# This creates and return a pointer to the devices collection
driver_collection = taxi_dbh[DRIVER_COLLECTION]
driver_collection.delete_many({})
with open(RELATIVE_CONFIG_PATH+DRIVER_COLLECTION+'.csv', 'r') as driver_fh:
    for driver_row in driver_fh:
        driver_row = driver_row.rstrip()
        if driver_row:
            (driverName, currentCabId, joinedDate) = driver_row.split(',')
        device_data = {'driverName': driverName, 'currentCabId': currentCabId, 'joinedDate': joinedDate}

        # This inserts the data item as a document in the devices collection
       # driver_collection.insert_one(device_data)


##Taxi collection to hold all the taxi information whihc are registerd with the TaxiApp
#returning pointer to device_access collection
taxi_collection = taxi_dbh[TAXI_COLLECTION]
taxi_collection.delete_many({})
with open(RELATIVE_CONFIG_PATH+TAXI_COLLECTION+'.csv','r') as taxis_fh:
    for taxi_row in taxis_fh:
        taxi_row = taxi_row.rstrip()
        if taxi_row:
            (reg_no, brand, model, type, base_rate, vacant, currentLat, currentLong) = taxi_row.split(',')
        currentCoordinates = {'type': "Point",'coordinates': [currentLat, currentLong]}
        taxi_data = {'reg_no': reg_no, 'brand': brand,'model': model, 'type':type, 'base_rate':base_rate, 'vacant':vacant, 'currentCoordinates':currentCoordinates }

        #inserting data item as a document in device access collection
       # taxi_collection.insert_one(taxi_data)
       '''

