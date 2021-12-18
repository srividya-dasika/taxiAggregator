from database import Database



class CollectionMapper:
    def __init__(self, city):
        self.city = city

    @property
    # To do, read the collection config from a config server
    def get_collection_name(self):
        print(f'Coming here??, {self.city}')
        if self.city.lower() == 'Hyderabad'.lower():
            self._db_collection = 'taxi_area_hyd'
            print(f'fetching data from {self._db_collection} collection')
        elif self.city.lower() == 'Thiruvananthapuram'.lower():
            self._db_collection = 'taxi_area_tvm'
            print(f'fetching data from {self._db_collection} collection')
        elif self.city.lower() == 'Pune City'.lower():
            self._db_collection = 'taxi_area_pune'
            print(f'fetching data from {self._db_collection} collection')
        else:
            print(f'Service Area {self.city} not Served currently! ')
            return

        return self._db_collection

    @property
    # To do, read the collection config from a config server
    def get_trip_collection_name(self):
        if self.city == 'Hyderabad':
            self._db_collection = 'trips_in_hyd'
            print(f'fetching data from {self._db_collection} collection')
        elif self.city == 'Thiruvananthapuram':
            self._db_collection = 'trips_in_tvm'
            print(f'fetching data from {self._db_collection} collection')
        elif self.city == 'Pune City':
            self._db_collection = 'trips_in_pune'
            print(f'fetching data from {self._db_collection} collection')
        else:
            print(f'Service Area {self.city} not Served currently! ')
            return

        return self._db_collection
