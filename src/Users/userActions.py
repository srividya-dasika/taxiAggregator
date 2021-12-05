from src.Taxi.taxiActions import Taxi

class Users:
    def __init__(self, username,userLocation):
        self.username = username
        self.location = userLocation

    def login(self,username): #check if user exists in db and if so , login successfully
        return 1

    def add_new_user(self,username,location): #Adding new user into DB.
        return 1

    def requestTaxi(self):
        #  Send request to book a taxi to the taxi service.
        #  Wait till a taxi is allotted.
        #  Then change user status to riding
        print(self.username," requested for taxi...")
        taxis = Taxi()
        nearbyTaxis = taxis.getNearestTaxis(self.username,self.location)
#        if self.checkDriverAvailability(nearbyTaxis[0]):
 #           taxis.updateTaxiStatus(nearbyTaxis[0].reg_no,"Occupied")


    def checkDriverAvailability(self,Taxi):
        return True

