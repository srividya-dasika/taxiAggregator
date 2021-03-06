from src.Utils.database import Database



class CollectionMapper:

    def __init__(self, city):
        self.city = city

    @property
    # To do, read the collection config from a config server
    def get_collection_name(self):

        if self.city == 'Hyderabad':
            self._db_collection = 'taxi_area_hyd'
            print(f'fetching data from {self._db_collection} collection' )
        elif self.city == 'Thiruvananthapuram':
            self._db_collection = 'taxi_area_tvm'
            print(f'fetching data from {self._db_collection} collection')
        elif self.city == 'Pune City':
            self._db_collection = 'taxi_area_pune'
            print(f'fetching data from {self._db_collection} collection')
        else:
            print(f'No collections found for {self.city}')
            return

        return self._db_collection
