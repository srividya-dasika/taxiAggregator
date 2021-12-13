from database import Database



class CollectionMapper:
    SERVICE_AREA_COLLECTION = 'service_area'
    def __init__(self, city):
        self.city = city

    @property
    # To do, read the collection config from a config server
    def get_collection_name(self):

        if self.city == 'Hyderabad':
            self._db_collection = 'service_area_hyd'
            print(self._db_collection )
        elif self.city == 'Thiruvananthapuram':
            self._db_collection = 'service_area_tvm'
            print(self._db_collection)
        elif self.city == 'Pune City':
            self._db_collection = 'service_area_pune'
        else:
            print("Service Area not Served currently! ")
            return

        return self._db_collection
