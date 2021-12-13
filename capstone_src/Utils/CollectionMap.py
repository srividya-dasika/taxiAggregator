from src.Utils.database import Database



class CollectionMapper:
    SERVICE_AREA_COLLECTION = 'service_area'
    def __init__(self, city):
        self.city = city

    @property
    # To do, read the collection config from a config server
    def get_collection_name(self):

        if self.city == 'Hyderabad':
            self._db_collection = 'taxi_location'
            print(self._db_collection )
        elif self.city == 'Thiruvananthapuram':
            self._db_collection = 'service_location_tvm'
            print(self._db_collection)
        elif self.city == 'Pune City':
            self._db_collection = 'service_location_pune'
        else:
            print("oops ")
            return

        return self._db_collection
