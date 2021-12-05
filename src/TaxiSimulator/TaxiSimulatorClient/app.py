from flask_cors import CORS
from flask import Flask, jsonify
from src.Taxi.taxiSimulation import processdata

app = Flask(__name__)
CORS(app)
# In this case, the URL route is 'displaylocations'.
@app.route('/displaylocations')
def displaylocations():
    # Obtain the CSV data.
    l = processdata()
    # Forward the data to the source that called this API.
    return jsonify(l)

if __name__ == '__main__':
    app.run(host = 'localhost', debug = True, port = 1112)
