from src.Utils.database import Database
# Imports ObjectId to convert to the correct format before querying in the db
from bson.objectid import ObjectId


class CollectionMapper:
    SERVICE_AREA_COLLECTION = 'service_area'
    def __init__(self, city):
        self.city = city

    @property
    def get_collection_name(self):

        return self._current_loc
