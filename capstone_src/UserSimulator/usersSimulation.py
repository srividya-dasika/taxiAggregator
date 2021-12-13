#Simulate user request.
# 1. Single requests from single user
# 2. Parallel requests from 3 users.
import threading
from src.Users.userActions import Users
from src.Location.locationService import Location

class UserSimulation:

    def simulateSingleUserRequest(self):
        user1Location = Location("Point", "Hyderabad", 17.387051, 78.486956)
        user1 = Users("user1", user1Location.current_loc)
        user1.requestTaxi('All')

    def simulateMultiUserRequest(self):
        # Out of service area
        user1Location = Location("Point", "Hyderabad", 17.2279, 78.486956)
        user1 = Users("user1", user1Location.current_loc)

        user2Location = Location("Point", "Hyderabad", 17.387051, 78.486956)
        user2 = Users("user2", user2Location.current_loc)

        user3Location = Location("Point", "Thiruvananthapuram", 8.509586, 76.929379)
        user3 = Users("user3", user3Location.current_loc)

        user4Location = Location("Point", "Pune City", 18.512494, 73.873726)
        user4 = Users("user4", user4Location.current_loc)

        user1.requestTaxi('All')

        # creating thread
        t1 = threading.Thread(target=user2.requestTaxi('Luxury'), args=())
        t2 = threading.Thread(target=user3.requestTaxi('Deluxe'), args=())
        t3 = threading.Thread(target=user4.requestTaxi('Deluxe'), args=())

        # starting thread 1
        t1.start()
        # starting thread 2
        t2.start()
        # starting thread 3
        t3.start()

        # wait until thread 1 is completely executed
        t1.join()
        # wait until thread 2 is completely executed
        t2.join()
        # wait until thread 2 is completely executed
        t3.join()
        # both threads completely executed
        print("Done!")

d= UserSimulation()
d.simulateMultiUserRequest()