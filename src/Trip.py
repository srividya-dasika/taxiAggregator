from database import Database
from CollectionMap import CollectionMapper
from sendNotification import SendNotifications
import datetime

class Trip():
    trip_counter = 1
    def __init__(self, city, taxi_reg_no, username,driver_name,startPoint,endPoint):
        self._db = Database()
        self._latest_error = ''
        self._city = city
        self._startPoint = startPoint
        self._endPoint = endPoint
        self._taxi_reg_no = taxi_reg_no
        self._customer_id = username
        self._driver_name = driver_name

    def __inc_counter(self):
        Trip.trip_counter = Trip.trip_counter+1
        return Trip.trip_counter

    def __get_trip_id(self, city):
        id = city[0:4] + '_'+ str(self.__inc_counter()) + '_'+ self._customer_id[0:5]
        return id

    def __insert_trip_data(self, trip_id, hireLong, hireLat, destLong, destLat):

        obj = CollectionMapper(self._city)
        self._collection = obj.get_trip_collection_name

        #key = {'trip_id': trip_id}
        #status = self._db.get_single_data(self._collection, key)
        #if status != None:
        #    return
        hire_point = {'type': "Point", 'coordinates': [hireLong, hireLat]}
        destination_point = {'type': "Point", 'coordinates': [destLong, destLat]}

        start_time = datetime.datetime.now()
        data = { 'trip_id':trip_id,
                  'rider_id': self._customer_id,
                  'taxi_reg_no': self._taxi_reg_no,
                  'start_location':hire_point,
                  'end_location': destination_point,
                  'trip_start' : start_time,
                  'trip_end' : 'In progress'
                  }
        print(data)
        status = self._db.insert_single_data(self._collection, data)
        if status != None:
            print(f'\nStarting Trip {trip_id}  Rider id: {self._customer_id} Taxi no: {self._taxi_reg_no} Start: {hire_point}  Dest:{destination_point} StartTime: {start_time}')
        else:
            print(f'Trip cannot start due to software issues :-0')



    def __update_trip_data(self, trip_id, hire_point=0, destination_point= 0, trip_state ='end'):
        obj = CollectionMapper(self._city)
        self._collection = obj.get_trip_collection_name
        end_time = datetime.datetime.now()

        search_key = {'trip_id': trip_id}
        update_key = {"$set": {'start_location': hire_point, 'end_location':destination_point}}
        # Update the trip_end time alone when the trip_state=='end'
        if trip_state == 'end':

            update_key = {"$set": {'trip_end': end_time}}

        status = self._db.updateOne(self._collection, search_key, update_key, upsert=False)
        print(f'Starting Ends {trip_id}  End time = {end_time}')
        return

    def start_trip(self, city, hireLong, hireLat, destLong, destLat):
        trip_id = self.__get_trip_id(city )
        self.__insert_trip_data(trip_id,  hireLong, hireLat, destLong, destLat)
        sns = SendNotifications()
        sns.sendNotification("trip started with "+trip_id,"Taxi App - Trip Start Message")
        return trip_id

    def end_trip(self, trip_id ):
        self.__update_trip_data(trip_id, trip_state='end')
        return



