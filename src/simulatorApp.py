from flask_cors import CORS
from flask import Flask, jsonify, request
from src.Taxi.taxiModel import *
from src.Users.userModel import *
from src.Drivers.driverModel import *
from src.TaxiSimulator.TaxiSimulatorClient.taxiSimulation import TaxiSimulator
from src.UserSimulator.usersSimulation import UserSimulation


app = Flask(__name__)
CORS(app)
@app.route("/setInitialTaxiCoords",methods = ['POST'])
def setInitialTaxiCoords():
    taxi_simulator = TaxiSimulator()
    CONFIG_PATH = "../config/"
    taxi_simulator.setInitialTaxiCoords(CONFIG_PATH+"50taxis.csv")
    return "Taxis Loaded!!"

@app.route("/simulateTaxis",methods = ['POST','GET'])
def simulateTaxis():
    taxi_simulator = TaxiSimulator()
    CONFIG_PATH = "../config/"
    taxi_simulator.simulateTaxis(CONFIG_PATH+"50taxis.csv")

