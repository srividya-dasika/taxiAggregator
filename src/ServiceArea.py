from database import Database

class ServiceArea:
    collection = 'service_area'

    def __init__(self):
        self._db = Database()
        self._latest_error = ''

    def is_service_area_defined(self, city):
        key = { "features.properties.name": city}

        ret = self._db.get_single_data(self.collection, key)
        if ret:
            print(f'Service area is defined for {city}')
            return True
        else:
            print(f'Service area is not yet defined')
            return False

    def create_service_area(self, service_area_def_file):
        return self._db.insert_single_data(self.collection, service_area_def_file)

    def find_service_area(self, usrlocation):
        self.long, self.lat = usrlocation['coordinates']
        print ('User location', self.long, self.lat, '\nCity specified by User is', usrlocation['city'])
        key = {
                "features.geometry": {
                    "$geoIntersects": {
                        "$geometry": {
                            "type": "Point",
                            "coordinates": [
                                self.long,
                                self.lat
                            ]
                        }
                    }
                }
            }
        ret= self._db.get_single_data(self.collection, key)
        if ret:
            print('Service area is ', ret['features'][0]['properties']['name'])
            return ret['features'][0]['properties']['name']
        return

    def validate_service_area(self, userlocation):

        service_city = self.find_service_area(userlocation)
        if userlocation['city'] == service_city:
            return True
        else:
            print('Selected city', userlocation['city'], 'or the selected coordinate ',userlocation['coordinates'] ,'is not within service area')
            return False

class ServiceAreaBoundary():

    def create_boundary(self, city, boundary_file):
        service_obj = ServiceArea()
        service_area_def = service_obj.is_service_area_defined(city)
        if service_area_def is False:
            service_obj.create_service_area(boundary_file)