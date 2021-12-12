from src.Location.locationService import Location
from src.Utils.database import Database
import random
import csv

class TaxiRegistration:
    taxi_brand= { 'Luxury':['Audi, BMW', 'Jaguar','Mercedes'],
                  'Deluxe' : ['Ecosport', 'skoda', 'Ciaz'],
                  'Basic': ['Zen','Tiago', 'Sonet' ]
                  }

    def __init__(self):
        self.geo_center = { 'lat': 18.5204, 'lon' : 73.8567}
        self.rand_lat_seed = self.geo_center['lat'] -0.3
        self.rand_lon_seed = self.geo_center['lon'] -0.3
        self.taxi_data =[]
    def generate_taxi_details(self):
        with open('taxi_reg_pune.csv', 'w', newline='') as csvfile:
            writer_handle = csv.writer(csvfile)
            for i in range(1, 2):
                lat = self.rand_lat_seed + random.random()
                long = self.rand_lon_seed + random.random()
                taxi_reg_no = 'MH12DX' + str(format(i, '04d'))
                taxi_type = random.choice(['Deluxe', 'Luxury', 'Basic'])
                loc_name = 'point' + str(i)
                #plot_coord.append([lat, long])
                taxi_info = ({'taxi_reg_no': taxi_reg_no,
                              'brand': random.choice(TaxiRegistration.taxi_brand[taxi_type]),
                              'model':random.choice([2016,2017,2018,2019,2020,2021]),
                              'taxi_type': taxi_type,
                              'base_rate' : random.choice([100, 150, 125]),
                              'vacant': random.choice(['vacant', 'hired']),
                              'location': {
                                  'type': "Point",
                                  'coordinates': [long, lat]},
                              'location_name': loc_name})
                print(taxi_info)

                self.taxi_data.append(taxi_info)
            writer_handle.writerow(self.taxi_data)
        db = Database()
        print(type(self.taxi_data))
        db.insert_many('service_area_pune',self.taxi_data)
        return taxi_info

obj = TaxiRegistration()
obj.generate_taxi_details()


