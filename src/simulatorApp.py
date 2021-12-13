from flask_cors import CORS
from flask import Flask
from src.TaxiSimulator.TaxiSimulatorClient.taxiSimulation import TaxiSimulator

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

