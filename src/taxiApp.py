from flask_cors import CORS
from flask import Flask, jsonify, request

from Location.locationService import Location
from Taxi.taxiModel import Taxi
from src.Taxi.taxiModel import TaxiModel

app = Flask(__name__)
CORS(app)
@app.route('/requestTaxi', methods = ['GET'])
def requestTaxi():
    #user1Location = Location("POINT", 10.12, 10.15)
    #user1 = Users("user1", user1Location.current_loc)
    #user1.requestTaxi('All')
    taxis = Taxi()
    userLocation = Location("Point", 17.2279, 79.00512)
    taxi_list = taxis.getNearestTaxis("user1",userLocation.current_loc,"Luxury")
    for taxi in taxi_list:
        print(taxi.reg_no)
    return "list of taxis - "


@app.route('/selectTaxi', methods=['POST', 'GET'])
def selectTaxi():
    taxi = Taxi()
    taxi.updateTaxiStatus("","")

if __name__ == '__main__':
    app.run(host = 'localhost', debug = True, port = 1113)





