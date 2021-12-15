from taxiModel import *
from userModel import *
from driverModel import *
from src.TaxiSimulator.TaxiSimulatorClient.taxiSimulation import TaxiSimulator
from usersSimulation import UserSimulation

user_coll = UserModel()
taxi_coll = TaxiModel()
driver_coll = DriverModel()
#Admin App - Taxi and user registration
#Register New User
user_coll.insertNewUser("user1","test@test.com","2021-10-10","male",1234123412,"test",10.1234,12.1234)

#Register New Taxi
taxi_coll.insertNewTaxi("ka12bs1234","Test","Test23","economy","true",30,12.1234,12.2334)

#Register Driver
driver_coll.insertNewDriver("driver1","email","2020-10-10","female",1234123412,"test2",17.8989,78.9999)

################################################################################
#Initial Area Creation - Defining the Rectangle


################################################################################
#Taxi Simulation
#Add 50 taxis
taxi_simulator = TaxiSimulator()
CONFIG_PATH = "config/"
#taxi_simulator.setInitialTaxiCoords(CONFIG_PATH+"50taxis.csv")
#taxi_simulator.simulateTaxis(CONFIG_PATH+"50taxis.csv")


################################################################################
#User Request Simulation
#Each user can make a request for a taxi at any time
user_simulator = UserSimulation()
user_simulator.simulateSingleUserRequest()
user_simulator.simulateMultiUserRequest()

#Ability to ingest taxi location information and user requests in a scalable way
#???