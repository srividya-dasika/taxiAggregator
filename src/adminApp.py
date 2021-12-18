from flask_cors import CORS
from flask import Flask, jsonify, request
from taxiModel import TaxiModel
from driverModel import DriverModel
from userModel import UserModel
from ServiceArea import ServiceAreaBoundary
import json
'''
application = Flask(__name__)
CORS(application)
@application.route('/createUser', methods = ['POST','GET'])
def createUser():
    user_coll = UserModel()
    # user_coll.insertNewUser("user1", "test@test.com", "2021-10-10", "male", '0417-1234123412', "Pune City", 10.1234, 12.1234 )
    # return "User added Successfully!"
    content_type = request.headers.get('Content-Type')
    if content_type == 'application/json':
        user_dict = request.json
        print("name=",user_dict['username'])
        user_coll.insertNewUser(user_dict['username'], user_dict['email'], user_dict['joinedDate'],user_dict['gender'], user_dict['mobileNumber'],
                                user_dict['location'] , user_dict['latitude'],user_dict['longitude'])
        return "User added Successfully!"
    else:
        return 'Content-Type not supported!'

@application.route('/createTaxi', methods = ['POST','GET'])
def createTaxi():
    taxi_coll = TaxiModel()
    content_type = request.headers.get('Content-Type')
    if content_type == 'application/json':
        taxi_dict = request.json
        taxi_coll.insertNewTaxi(taxi_dict['taxi_reg_no'],taxi_dict['brand'],taxi_dict['model'],taxi_dict['taxi_type'],taxi_dict['base_rate'],
                                taxi_dict['vacant'],taxi_dict['latitude'],taxi_dict['longitude'], taxi_dict['location_name'])
        return "Taxi added Successfully!"
    else:
        return 'Content-Type not supported!'

@application.route('/createDriver', methods = ['POST','GET'])
def createDriver():
    driver_coll = DriverModel()
    content_type = request.headers.get('Content-Type')
    if content_type == 'application/json':
        driver_dict = request.json
        driver_coll.insertNewDriver(driver_dict['driverName'], driver_dict['email'], driver_dict['joinedDate'], driver_dict['gender'],
                                    driver_dict['mobileNumber'],  driver_dict['latitude'], driver_dict['longitude'], driver_dict['location'])
        return "Driver added Successfully!"
    else:
        return 'Content-Type not supported!'
'''
def createServiceAreaBoundaries(geoJsonFile):
    Service_area_boundary_obj = ServiceAreaBoundary()

    with open(geoJsonFile) as f:
        data = f.read()
        js = json.loads(data)
        city = js['features'][0]['properties']['name']
        create_result = Service_area_boundary_obj.create_boundary(city, js)
        if create_result != None:
            print (f'Service area boundary created for {city}')

#if __name__ == '__main__':
#    application.run(host = 'localhost', debug = True, port = 1112)

createServiceAreaBoundaries('Pune City.geojson')
createServiceAreaBoundaries('Hyderabad.geojson')
createServiceAreaBoundaries('Thiruvananthapuram.geojson')