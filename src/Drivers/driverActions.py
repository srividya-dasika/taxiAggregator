class Driver:
    def __init__(self, drivername,cabid):
        self.drivername = drivername
        #self.location = location

    def login(self,username): #check if user exists in db and if so , login successfully
        return 1
    def add_new_driver(self,username,location): #Adding new user into DB.
        return 1

    def acceptTaxiRequest(self,username):
        #  Send request to book a taxi to the taxi service.
        #  Wait till a taxi is allotted.
        #  Then change user status to riding
        print(self.drivername," accepted the request from ",username)

