'''
This file serves as the backend for the Taxi Application which primarily serves all the user requests.
'''
from flask_cors import CORS
from flask import Flask, request, jsonify

from locationService import Location
from taxiModel import Taxi
from userModel import Users
from driverModel import Driver
from Trip import Trip

application = Flask(__name__)
CORS(application)

# API implementation for a user to request for taxi.
# Takes the username, TaxiType as input and returns the list of nearest Taxis by querying the taxi collection basing on the proximity, taxi type, and taxi availability
@application.route('/requestTaxi', methods = ['GET','POST'])
def requestTaxi():
    #user1Location = Location("POINT", 10.12, 10.15)
    #user1 = Users("user1", user1Location.current_loc)
    #user1.requestTaxi('All')
    taxis = Taxi()
    content_type = request.headers.get('Content-Type')
    if content_type == 'application/json':
        taxi_request_dict = request.json
        user = Users(taxi_request_dict['userName'], taxi_request_dict['location'])
        userLoc = user.get_user_currentCoordinates(taxi_request_dict['userName'])
        userLocation = Location("Point", taxi_request_dict['location'],userLoc['coordinates'][0], userLoc['coordinates'][1])
        taxi_list = taxis.getNearestTaxis(taxi_request_dict['userName'],userLocation.current_loc,taxi_request_dict['taxiType'])
        if taxi_list==-1:
            return "Error: Either city name is incorrect or user location is not in our service area"
        elif taxi_list == []:
            return "No Nearby taxis found"
        else:
            return jsonify(taxi_list)
    else :
        return 'Content-Type not supported!'

# Provides a mechanism for user to select a taxi from the list of taxis returned in the requestTaxi end point.No validationsin placeat this point of time.
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
        print(f'if userName = {userName} or driverName = {driverName} or taxiRegNo = {taxiRegNo}')
        if userName == -1 or driverName ==-1 or taxiRegNo == -1:
            return f'Something went wrong, could not select the taxi for user. Please try again later...'
        else:
            return f'Taxi selected SuccessFully with user -{userName} & driver -{driverName} , On Taxi -{taxiRegNo} ! Proceed to Start Trip...'
    else:
        return 'Content-Type not supported!'

# API implementation for starting the trip. Expects the user to send username,taxiname and driver name. And in the backend sets the onTrip status of user and driver to True and changes the taxi vacancy status to booked.
# Also triggers a notification to user and Driver to let them know about the trip start
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

# API implementatino for end of the trip. Resets the user,driver and taxi status to represent they are not on trip and the updates the taxi and users co-ordinates as per destination co-ordinates. Also can be extended to send trip end notifications.
@application.route('/endTrip', methods=['POST', 'GET'])
def endTrip():
    content_type = request.headers.get('Content-Type')
    if content_type == 'application/json':
        trip_dict = request.json
        currentCoordinates = Location("Point", trip_dict['city'],trip_dict['currentLong'], trip_dict['currentLat'])
        trip_id = trip_dict['trip_id']
        trip = Trip(trip_id)
        end_status = trip.end_trip(trip_dict['city'], trip_id)
        if end_status == -1:
            return f'Trip end status could not be updated because of some error..please try in some time.'
        else:
            return f'Trip with id - {trip_id} ended ...Thanks for your trip!'
    else:
        return 'Content-Type not supported!'


if __name__ == '__main__':
    application.run(host = 'localhost', debug = True, port = 1113)





