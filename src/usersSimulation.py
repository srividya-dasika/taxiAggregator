#Simulate user request.
# 1. Single requests from single user
# 2. Parallel requests from 3 users.
import threading
from userModel import Users
from locationService import Location
from taxiModel import  Taxi

class UserSimulation:

    def simulateSingleUserRequest(self):
        user1Location = Location("Point", "Hyderabad", 17.387051, 78.486956)
        user1 = Users("user1", user1Location.current_loc)
        user1.requestTaxi('All')

    def simulateBookTaxi(self, user, taxi_type):
        taxi_list  = user.requestTaxi(taxi_type)
        returned_list =[]
        if taxi_list == None:
            print('No taxis found')
            return
        if len(list(taxi_list.clone())) == 0:
            print(f'No taxis found in proximity')
            return
        for taxi in taxi_list:
            returned_list.append(taxi)
            print(f'Taxi available :  {taxi}')

        selected_Taxi = returned_list[0]
        print('\nUser request for ',selected_Taxi)

        city = selected_Taxi['location_name']
        taxi_reg_no = selected_Taxi['taxi_reg_no']
        taxi_coord = selected_Taxi['currentCoordinates']['coordinates']
        user_coord = user.get_user_location()

        # First move to user location
        status = user.confirmTaxiBooking( city, taxi_reg_no, taxi_coord, user_coord)
        if status == 1:
            print(f'Booked taxi {taxi_reg_no}.. Taxi will arrive at your location{user_coord} soon')
        else:
            print(f'Booking could not be confirmed. Please try booking again')

        #Simulate taxi action also
        taxi_obj = Taxi()
        trip_id = taxi_obj.startTrip(city,taxi_reg_no,'9876543210', taxi_coord, user_coord )
        taxi_obj.endTrip(trip_id)


        status = user.confirmTripCompletion( city, taxi_reg_no, user_coord, user_coord)
        print("Taxi completed the trip and is back to vacant status")



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
        #t1 = threading.Thread(target=user2.requestTaxi('Luxury'), args=())
        t1 = threading.Thread(target=self.simulateBookTaxi(user2, 'Luxury'), args=())
        t2 = threading.Thread(target=self.simulateBookTaxi(user3,'All'), args=())
        t3 = threading.Thread(target=self.simulateBookTaxi(user4, 'All'), args=())

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