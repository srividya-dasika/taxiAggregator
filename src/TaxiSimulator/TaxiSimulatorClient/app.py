from flask_cors import CORS
from flask import Flask, jsonify, request
from taxiSimulation import TaxiSimulator
from taxiModel import TaxiModel
from locationService import Location

app = Flask(__name__)
CORS(app)
# In this case, the URL route is 'userlocations'.
@app.route('/userInitialLocations', methods = ['GET','POST'])
def userInitiallocations():
    # Obtain the CSV data.
    taxiSim = TaxiSimulator()
    content_type = request.headers.get('Content-Type')
    if content_type == 'application/json':
        area_dict = request.json
        userLocation = Location("Point", area_dict['location'], area_dict['currentLat'],
                                area_dict['currentLong'])
        userlocationsList = taxiSim.getInitialUserLocations(userLocation.current_loc,1000,10)
        # Forward the data to the source that called this API.
        return jsonify(userlocationsList)
    else :
        return 'Content-Type not supported!'


# In this case, the URL route is 'userlocations'.
@app.route('/areabounds', methods = ['GET','POST'])
def areabounds():
    # Obtain the CSV data.
    taxiSim = TaxiSimulator()
    l = taxiSim.processdata('../../../config/area_boundaries.csv')
    # Forward the data to the source that called this API.
    return jsonify(l)

@app.route('/taxiInitiallocations', methods = ['GET','POST'])
def taxiInitialLocations():
    # Obtain the CSV data.
    taxiSim = TaxiSimulator()
    content_type = request.headers.get('Content-Type')
    if content_type == 'application/json':
        area_dict = request.json
        taxiLocations = Location("Point", area_dict['location'], area_dict['currentLat'],
                                area_dict['currentLong'])
        userlocationsList = taxiSim.getInitialTaxiLocations(taxiLocations.current_loc,1000,100,"All")
        # Forward the data to the source that called this API.
        return jsonify(userlocationsList)
    else :
        return 'Content-Type not supported!'

@app.route('/taxiCurrentLocations/<string:taxiRegNo>', methods = ['GET','POST'])
def taxiCurrentLocations(taxiRegNo):
    sim = TaxiSimulator()
    return sim.getTaxiCurrentCoords(taxiRegNo)

# Obsolete
@app.route('/gettaxilocation', methods = ['GET','POST'])
def taxiroutes():
    # Obtain the CSV data.
    sim = TaxiSimulator
    l = sim.processdata('../../../config/taxi_routes.csv')
    # Forward the data to the source that called this API.
    return jsonify(l)

# Obsolete
@app.route('/settaxicoords/<string:taxiDetails>', methods=['POST', 'PUT', 'GET'])
def setTaxiCoords(taxiDetails):
    taxiModel = TaxiModel()
    print("PRinting request taxiname=",taxiDetails.split('&')[0]," lat=",taxiDetails.split('&')[1],"long=",taxiDetails.split('&')[2])
    taxiModel.upsertTaxiCoords(taxiDetails.split('&')[0],taxiDetails.split('&')[1],taxiDetails.split('&')[2])
    return 'DataSet'


if __name__ == '__main__':
    app.run(host = 'localhost', debug = True, port = 1112)
