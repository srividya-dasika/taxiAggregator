class Taxi:
    proximityRadius = 3 #assuming proximity factor as 3 kms.

    def __init__(self, reg_no=0):
        self.reg_no = reg_no
        #self.location = location

    def add_new_taxi(self,taxi_reg_no,location): #Adding new user into DB.
        return 1

    def getNearestTaxis(self,username,userLocation):
        #  Send request to book a taxi to the taxi service.
        #  Wait till a taxi is allotted.
        #  Then change user status to riding
        print("Fetching taxis nearby ",username)

        return
        #Mongoquery to get all nearby taxis.


    def updateTaxiStatus(self,reg_no, status):
        print("Taxi with ",self.reg_no," status changed to ",status)