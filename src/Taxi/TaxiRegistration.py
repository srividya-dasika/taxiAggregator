from src.Location.locationService import Location
from src.Utils.database import Database
from src.Utils.CollectionMap import CollectionMapper
import random
import csv

class TaxiRegistration:
    NUMBER_OF_USERS = 30


    #def __init__(self):

    taxi_data = []
    def generate_taxi_details(self, loc_name):
        with open('../TaxiSimulator/TaxiSimulatorClient/taxi_reg_tvm.csv', 'w', newline='') as csvfile:
            taxi_brand = {'Luxury': ['Audi, BMW', 'Jaguar', 'Mercedes'],
                          'Deluxe': ['Ecosport', 'skoda', 'Ciaz'],
                          'Basic': ['Zen', 'Tiago', 'Sonet']
                          }
            geo_center = {'Pune City': [18.5204, 73.8567], 'Hyderabad': [17.3850, 78.4867],
                               'Thiruvananthapuram': [8.5241, 76.9366]}

            state_prefix = {'Pune City': 'MH', 'Hyderabad': 'AP', 'Thiruvananthapuram': 'KL'}

            writer_handle = csv.writer(csvfile)
            for i in range(1, TaxiRegistration.NUMBER_OF_USERS):
                #loc_name = random.choice(['Pune City', 'Hyderabad', 'Thiruvananthapuram'])
                rand_lat_seed = geo_center[loc_name][0] - 0.3
                rand_lon_seed = geo_center[loc_name][1] - 0.3

                lat = rand_lat_seed + random.random()
                long = rand_lon_seed + random.random()
                taxi_reg_no = state_prefix[loc_name] + '01BX' + str(format(i, '04d'))
                taxi_type = random.choice(['Deluxe', 'Luxury', 'Basic'])
                brand = random.choice(taxi_brand[taxi_type])
                model = random.choice([2016,2017,2018,2019,2020,2021])
                base_rate = random.choice([100, 150, 125])
                vacant = 'vacant'

                #plot_coord.append([lat, long])

                taxi_info = ({'taxi_reg_no': taxi_reg_no,
                              'brand': brand,
                              'model':model,
                              'taxi_type': taxi_type,
                              'base_rate' : base_rate,
                              'vacant': vacant,
                              'location': {
                                  'type': "Point",
                                  'coordinates': [long, lat]},
                              'location_name': loc_name})
                print( f'{taxi_reg_no}, {brand}, {model}, {taxi_type}, {base_rate}, {vacant}, {lat}, {long}, {loc_name}')

                self.taxi_data.append(taxi_info)
            writer_handle.writerow(self.taxi_data)
        db = Database()
        print(type(self.taxi_data))
        obj = CollectionMapper(loc_name)
        collection =obj.get_collection_name
        db.insert_many(collection,self.taxi_data)
        return taxi_info

obj = TaxiRegistration()
obj.generate_taxi_details('Pune City')


