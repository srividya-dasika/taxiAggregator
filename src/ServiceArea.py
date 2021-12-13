from database import Database

class ServiceArea:
    collection = 'service_area'
    def __init__(self):
        self._db = Database()
        self._latest_error = ''

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