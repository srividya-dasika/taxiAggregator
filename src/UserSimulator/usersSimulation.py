#Simulate user request.
# 1. Single requests from single user
# 2. Parallel requests from 3 users.
import threading
from src.Users.userActions import Users
from src.Location.locationService import Location

class UserSimulation:

    def simulateSingleUserRequest(self):
        user1Location = Location("POINT", 10.12, 10.15)
        user1 = Users("user1", user1Location.current_loc)
        user1.requestTaxi('All')

    def simulateMultiUserRequest(self):
        user1Location = Location("Point", 17.2279, 79.00512)
        user1 = Users("user1", user1Location.current_loc)
        user2 = Users("user2", user1Location.current_loc)
        user3 = Users("user3", user1Location.current_loc)
        # creating thread
        t1 = threading.Thread(target=user2.requestTaxi('Luxury'), args=())
        t2 = threading.Thread(target=user3.requestTaxi('Deluxe'), args=())

        # starting thread 1
        t1.start()
        # starting thread 2
        t2.start()

        # wait until thread 1 is completely executed
        t1.join()
        # wait until thread 2 is completely executed
        t2.join()

        # both threads completely executed
        print("Done!")
