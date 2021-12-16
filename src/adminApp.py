from flask_cors import CORS
from flask import Flask, jsonify, request
from src.Users.userModel import UserModel
from src.Taxi.taxiModel import TaxiModel
from src.Drivers.driverModel import DriverModel
from src.Utils.ServiceAreaBoundary import ServiceAreaBoundary
import json

app = Flask(__name__)
CORS(app)
@app.route('/createUser', methods = ['POST','GET'])
def createUser():
    user_coll = UserModel()
    user_coll.insertNewUser("Theertha", "tsfan@test.com", "2021-12-10", "Feale", '0417-12223412', "Pune City", 10.6234, 97.15534 )
    return "User added Successfully!"

@app.route('/createTaxi', methods = ['POST','GET'])
def createTaxi():
    taxi_coll = TaxiModel()
    '''
    {'taxi_reg_no': taxi_reg_no,
      'brand': brand,
      'model':model,
      'taxi_type': taxi_type,
      'base_rate' : base_rate,
      'vacant': vacant,
      'location': {
          'type': "Point",
          'coordinates': [long, lat]},
      'location_name': loc_name}
    '''
    taxi_coll.insertNewTaxi("ka12bs1234","Indica",'2006',"Basic","120","vacant",12.1234,12.2334, "Hyderabad")

    return "Taxi added Successfully!"

@app.route('/createDriver', methods = ['POST','GET'])
def createDriver():
    driver_coll = DriverModel()
    driver_coll.insertNewDriver("Sasi", "sasi@gmail.com", "2020-10-12", "Female", 9876543210,  17.8989, 78.9999, "Hyderabad")
    return "Driver added Successfully!"


def createServiceAreaBoundaries():
    Service_area_boundary_obj = ServiceAreaBoundary()

    with open('Pune City.geojson') as f:
        data = f.read()
        js = json.loads(data)
        city = js['features'][0]['properties']['name']
        create_result = Service_area_boundary_obj.create_boundary(city, js)
        if create_result != None:
            print (f'Service area boundary created for {city}')
'''
if __name__ == '__main__':
    app.run(host = 'localhost', debug = True, port = 1112)

'''

createServiceAreaBoundaries()
createUser()
createTaxi()
createDriver()