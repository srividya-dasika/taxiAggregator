from src.Taxi.taxiModel import TaxiModel
import time
class Taxi:
    proximityRadius = 10 #assuming proximity factor as 3 kms.

    def __init__(self, reg_no=0):
        self.reg_no = reg_no
        #self.location = location
        self.taxi_model = TaxiModel()

    def add_new_taxi(self,taxi_reg_no,location): #Adding new user into DB.
        return 1

    def getNearestTaxis(self,username,userLocation):
        #  Send request to book a taxi to the taxi service.
        #  Wait till a taxi is allotted.
        #  Then change user status to riding
        print("Fetching taxis nearby ",username)

        #Mongoquery to get all nearby taxis.
        taxi_list = self.taxi_model.find_by_proximity(userLocation, self.proximityRadius)
        if taxi_list is None:
            print(f'No taxis found in {self.proximityRadius} km radius')
        for taxi in taxi_list:
            print(taxi)
        return taxi_list


    def updateTaxiStatus(self,reg_no, status):
        print("Taxi with ",self.reg_no," status changed to ",status)