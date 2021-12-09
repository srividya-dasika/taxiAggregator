class Location:

    def __init__(self,type,city,startLat,startLong,endLat=0,endLong=0):
        self.type = type
        self.startLat = startLat
        self.startLong = startLong
        self.endLad = endLat
        self.endLong = endLong
        self.city = city

    @property
    def current_loc(self):
        loc = [self.startLong, self.startLat]
        #Note:  Mongodb expects coord with longitude first and then latitude
        self._current_loc = {
                        'type': "Point",
                        'coordinates': loc,
                        'city': self.city
                    }
        return self._current_loc




