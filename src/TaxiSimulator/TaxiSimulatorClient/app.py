from flask_cors import CORS
from flask import Flask, jsonify
from taxiSimulation import processdata
from taxiModel import TaxiModel

app = Flask(__name__)
CORS(app)
# In this case, the URL route is 'userlocations'.
@app.route('/userlocations')
def userlocations():
    # Obtain the CSV data.
    l = processdata('../../../config/user_locations.csv')
    # Forward the data to the source that called this API.
    return jsonify(l)

# In this case, the URL route is 'userlocations'.
@app.route('/areabounds')
def areabounds():
    # Obtain the CSV data.
    l = processdata('../../../config/area_boundaries.csv')
    # Forward the data to the source that called this API.
    return jsonify(l)

# In this case, the URL route is 'taxiroutes'.
@app.route('/gettaxiroutes')
def taxiroutes():
    # Obtain the CSV data.
    l = processdata('../../../config/taxi_routes.csv')
    # Forward the data to the source that called this API.
    return jsonify(l)

# update Taxi location in DB
@app.route('/settaxicoords/<string:taxiDetails>', methods=['POST', 'PUT', 'GET'])
def setTaxiCoords(taxiDetails):
    taxiModel = TaxiModel()
    print("PRinting request taxiname=",taxiDetails.split('&')[0]," lat=",taxiDetails.split('&')[1],"long=",taxiDetails.split('&')[2])
    taxiModel.upsertTaxiCoords(taxiDetails.split('&')[0],taxiDetails.split('&')[1],taxiDetails.split('&')[2])
    return 'DataSet'


if __name__ == '__main__':
    app.run(host = 'localhost', debug = True, port = 1112)
