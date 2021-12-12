from src.Taxi.taxiModel import TaxiModel
from src.Utils.CollectionMap import CollectionMapper
from src.Utils.ServiceArea import ServiceArea
import time
class Taxi:
    proximityRadius = 1000 #assuming proximity factor as 3 kms.
    searchResultLimit = 5   # limit the number of search results
    def __init__(self, reg_no=0):
        self.reg_no = reg_no
        #self.location = location
        self.taxi_model = TaxiModel()

    def add_new_taxi(self,taxi_reg_no,location): #Adding new user into DB.
        return 1

    def getNearestTaxis(self,username,userLocation, taxi_type):
        #  Send request to book a taxi to the taxi service.
        #  Wait till a taxi is allotted.
        #  Then change user status to riding
        print("Fetching taxis nearby for ",username)
        #try:
        obj_serv = ServiceArea()
        within_service_area = obj_serv.validate_service_area(userLocation)

        if within_service_area:

            #Mongoquery to get all nearby taxis.
            taxi_list = self.taxi_model.find_by_proximity( userLocation, self.proximityRadius, self.searchResultLimit, taxi_type)
            #print((taxi_list))
            if len(list(taxi_list.clone())) == 0:
                print(f'No taxis found in {self.proximityRadius} km radius')
            for taxi in taxi_list:
                print(taxi)
            return taxi_list
        #except:
        else:
            print('Error: Either city name is incorrect or user location is not in our service area')


    def updateTaxiStatus(self,reg_no, status):
        print("Taxi with ",self.reg_no," status changed to ",status)
        return self.taxi_model.update_one(reg_no, status)


