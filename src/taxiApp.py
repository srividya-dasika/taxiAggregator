from flask_cors import CORS
from flask import Flask, request

from locationService import Location
from taxiModel import Taxi

app = Flask(__name__)
CORS(app)
@app.route('/requestTaxi', methods = ['GET','POST'])
def requestTaxi():
    #user1Location = Location("POINT", 10.12, 10.15)
    #user1 = Users("user1", user1Location.current_loc)
    #user1.requestTaxi('All')
    taxis = Taxi()
    content_type = request.headers.get('Content-Type')
    if content_type == 'application/json':
        taxi_request_dict = request.json
        userLocation = Location("Point", taxi_request_dict['location'],taxi_request_dict['currentLat'], taxi_request_dict['currentLong'])
        taxi_list = taxis.getNearestTaxis(taxi_request_dict['userName'],userLocation.current_loc,taxi_request_dict['taxiType'])
        for taxi in taxi_list:
            print(taxi.reg_no)
        return "List of Taxis.."
    else :
        return 'Content-Type not supported!'


@app.route('/selectTaxi', methods=['POST', 'GET'])
def selectTaxi():
    content_type = request.headers.get('Content-Type')
    if content_type == 'application/json':
        selected_taxi_dict = request.json
        taxi = Taxi()
        taxi.updateTaxidStatus(selected_taxi_dict['taxiRegNo'],"occupied")
        return "Trip started!"
    else:
        return 'Content-Type not supported!'

@app.route('/getTaxiCoords', methods=['POST', 'GET'])
def getTaxiCoords():
    return

if __name__ == '__main__':
    app.run(host = 'localhost', debug = True, port = 1113)





