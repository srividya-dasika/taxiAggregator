from flask_cors import CORS
from flask import Flask, request, jsonify

from locationService import Location
from taxiModel import Taxi

application = Flask(__name__)
CORS(application)
@application.route('/requestTaxi', methods = ['GET','POST'])
def requestTaxi():
    #user1Location = Location("POINT", 10.12, 10.15)
    #user1 = Users("user1", user1Location.current_loc)
    #user1.requestTaxi('All')
    taxis = Taxi()
    content_type = request.headers.get('Content-Type')
    if content_type == 'application/json':
        taxi_request_dict = request.json
        userLocation = Location("Point", taxi_request_dict['location'],taxi_request_dict['currentLong'], taxi_request_dict['currentLat'])
        taxi_list = taxis.getNearestTaxis(taxi_request_dict['userName'],userLocation.current_loc,taxi_request_dict['taxiType'])
        if taxi_list==-1:
            return "Error: Either city name is incorrect or user location is not in our service area"
        elif taxi_list == []:
            return "No Nearby taxis found"
        else:
            return jsonify(taxi_list)
    else :
        return 'Content-Type not supported!'


@application.route('/selectTaxi', methods=['POST', 'GET'])
def selectTaxi():
    content_type = request.headers.get('Content-Type')
    if content_type == 'application/json':
        selected_taxi_dict = request.json
        taxi = Taxi()
        taxi.updateTaxidStatus(selected_taxi_dict['taxiRegNo'],"occupied")
        return "Trip started!"
    else:
        return 'Content-Type not supported!'

@application.route('/getTaxiCoords', methods=['POST', 'GET'])
def getTaxiCoords():
    return

if __name__ == '__main__':
    application.run(host = 'localhost', debug = True, port = 1113)





