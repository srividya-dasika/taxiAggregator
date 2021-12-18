from flask_cors import CORS
from flask import Flask, request, jsonify

from locationService import Location
from taxiModel import Taxi
from userModel import Users
from driverModel import Driver
from Trip import Trip

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
        user = Users(selected_taxi_dict["user_name"],selected_taxi_dict["city"])
        driver = Driver()
        userName = user.updateUserStatus(selected_taxi_dict["user_name"],selected_taxi_dict['taxi_reg_no'],False,True)
        driverName = driver.updateDriverStatus("",selected_taxi_dict['taxi_reg_no'],False,True)
        taxiRegNo = taxi.updateTaxiStatus(selected_taxi_dict["city"],selected_taxi_dict["user_name"],selected_taxi_dict['taxi_reg_no'],"vacant","booked")
        if userName == -1 or driverName ==-1 or taxiRegNo == -1:
            return f'Something went wrong, could not select the taxi for user. Please try again later...'
        else:
            return f'Taxi selected SuccessFully with user -{userName} & driver -{driverName} , On Taxi -{taxiRegNo} ! Proceed to Start Trip...'
    else:
        return 'Content-Type not supported!'

@application.route('/startTrip', methods=['POST', 'GET'])
def startTrip():
    content_type = request.headers.get('Content-Type')
    if content_type == 'application/json':
        trip_dict = request.json
        #alternatively we can get user coordinates from db
        currentCoordinates = Location("Point", trip_dict['city'],trip_dict['currentLong'], trip_dict['currentLat'])
        destinationCoordinates = Location("Point", trip_dict['city'],trip_dict['destLong'], trip_dict['destLat'])
        trip = Trip(trip_dict["city"],trip_dict["taxi_reg_no"],trip_dict["username"],trip_dict["driver_name"],
                    currentCoordinates,destinationCoordinates)
        trip_id = trip.start_trip(trip_dict['city'],trip_dict['currentLong'], trip_dict['currentLat'],trip_dict['destLong'], trip_dict['destLat'])
        if trip_id == -1:
            return f'Trip could not start because of some error..please try in some time.'
        else:
            return f'Trip with id - {trip_id} started successfully...enjoy your trip!'
    else:
        return 'Content-Type not supported!'



@application.route('/getTaxiCoords', methods=['POST', 'GET'])
def getTaxiCoords():
    return

if __name__ == '__main__':
    application.run(host = 'localhost', debug = True, port = 1113)





