'''
The taxi simulator app APIs
This files serves as the backend service for the UI Simulation of Users,Taxis and TaxiMovement via the Google Maps integration.
'''
from flask_cors import CORS
from flask import Flask, jsonify, request
from taxiSimulation import TaxiSimulator
from taxiModel import TaxiModel
from locationService import Location

application = Flask(__name__)
CORS(application)
# API to fetch the initial user locations. It returns all the users in the DB as of now. Can be extended to users in a specific area in future
# In this case, the URL route is 'userlocations'.
@application.route('/userInitialLocations', methods = ['GET','POST'])
def userInitiallocations():
    # Obtain the CSV data.
    taxiSim = TaxiSimulator()
    content_type = request.headers.get('Content-Type')
    if content_type == 'application/json':
        area_dict = request.json
        currentArea = Location("Point", area_dict['location'], area_dict['currentLat'], area_dict['currentLong']
                                )
        userlocationsList = taxiSim.getInitialUserLocations(currentArea.current_loc,100000000,10)
        # Forward the data to the source that called this API.
        return jsonify(userlocationsList)
    else :
        return 'Content-Type not supported!'

# API to get the initial Area Bounds. This will help in representing the Area boundary in the UI (google map implementation)
# In this case, the URL route is 'areabounds'.
@application.route('/areabounds', methods = ['GET','POST'])
def areabounds():
    # Obtain the CSV data.
    taxiSim = TaxiSimulator()
    l = taxiSim.processdata('../config/area_boundaries.csv')
    # Forward the data to the source that called this API.
    return jsonify(l)

# API to get the initial taxi locations. This will help in representing all the taxis in the service area at the start of the simulation.
# In this case, the URL route is '/taxiInitiallocations'
@application.route('/taxiInitiallocations', methods = ['GET','POST'])
def taxiInitialLocations():
    # Obtain the CSV data.
    taxiSim = TaxiSimulator()
    content_type = request.headers.get('Content-Type')
    if content_type == 'application/json':
        area_dict = request.json
        currentArea = Location("Point", area_dict['location'], area_dict['currentLat'],
                                area_dict['currentLong'])
        taxilocationsList = taxiSim.getInitialTaxiLocations(currentArea.current_loc,100000,100,"All")
        # Forward the data to the source that called this API.
        return jsonify(taxilocationsList)
    else :
        return 'Content-Type not supported!'

# API to get the current taxi locations. This method will help in plotting the taxi route on the Google Map
# Input - Taxi_reg_no and City name,Output - Taxi Current Location co-ordinates
# In this case, the URL route is '/taxiCurrentLocations'
@application.route('/taxiCurrentLocations/', methods = ['GET','POST'])
def taxiCurrentLocations():
    sim = TaxiSimulator()
    content_type = request.headers.get('Content-Type')
    if content_type == 'application/json':
        taxi_dict = request.json
        taxidata = sim.getTaxiCurrentCoords(taxi_dict['reg_no'],taxi_dict['location'])
        return jsonify(taxidata)
    else :
        return 'Content-Type not supported!'


# Obsolete
@application.route('/gettaxilocation', methods = ['GET','POST'])
def taxiroutes():
    # Obtain the CSV data.
    sim = TaxiSimulator
    l = sim.processdata('../../../config/taxi_routes.csv')
    # Forward the data to the source that called this API.
    return jsonify(l)

# Obsolete
@application.route('/settaxicoords/<string:taxiDetails>', methods=['POST', 'PUT', 'GET'])
def setTaxiCoords(taxiDetails):
    taxiModel = TaxiModel()
    print("PRinting request taxiname=",taxiDetails.split('&')[0]," lat=",taxiDetails.split('&')[1],"long=",taxiDetails.split('&')[2])
    taxiModel.upsertTaxiCoords(taxiDetails.split('&')[0],taxiDetails.split('&')[1],taxiDetails.split('&')[2])
    return 'DataSet'


if __name__ == '__main__':
    application.run(host = 'localhost', debug = True, port = 1112)
