from flask_cors import CORS
from flask import Flask, jsonify, request
from src.Users.userModel import UserModel
from src.Taxi.taxiModel import TaxiModel
from src.Drivers.driverModel import DriverModel


app = Flask(__name__)
CORS(app)
@app.route('/createUser', methods = ['POST','GET'])
def createUser():
    user_coll = UserModel()
    user_coll.insertNewUser("user1", "test@test.com", "2021-10-10", "male", 1234123412, "test", 10.1234, 12.1234)
    return "User added Successfully!"


@app.route('/createTaxi', methods = ['POST','GET'])
def createTaxi():
    taxi_coll = TaxiModel()
    taxi_coll.insertNewTaxi("ka12bs1234","Test","Test23","economy","true",30,12.1234,12.2334)
    return "Taxi added Successfully!"

@app.route('/createDriver', methods = ['POST','GET'])
def createDriver():
    driver_coll = DriverModel()
    driver_coll.insertNewDriver("driver1", "email", "2020-10-10", "female", 1234123412, "test2", 17.8989, 78.9999)
    return "Driver added Successfully!"

if __name__ == '__main__':
    app.run(host = 'localhost', debug = True, port = 1112)