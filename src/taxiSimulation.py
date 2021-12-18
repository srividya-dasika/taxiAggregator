import time

import pandas as pd
import threading
from taxiModel import TaxiModel
from userModel import UserModel

class TaxiSimulator:

    def processdata(self,fileToProcess):
        # Loading and reading the CSV file.
        df = pd.read_csv(fileToProcess, delimiter =',')
        # Converting the CSV data to a list.
        df = df.to_dict(orient = 'records')
        return df

    def getInitialUserLocations(self,location,proximity,search_limit):
        user = UserModel()
        print(f'getting users in the area...{location}')
        userData = user.get_nearby_users(location,proximity,search_limit)
        print(f'Got Data from DB {userData}')
        docs = list(userData)
        user_dict = []
        print("nJSON data:", docs)
        for doc in docs:
            Dict = {'userName': doc['username'], 'latitude':doc['currentCoordinates'].get('coordinates')[1],'longitude':doc['currentCoordinates'].get('coordinates')[0]}
            user_dict.append(Dict)
        return user_dict

    def getInitialTaxiLocations(self,location,proximity,search_limit,type):
        taxis = TaxiModel()
        print(f'getting all taxis in the area...{location}')
        taxiData = taxis.getAllTaxisInArea(location,proximity,search_limit)
        print(f'Got Taxi Data from DB {taxiData}')
        docs = list(taxiData)
        taxi_dict = []
        print("Taxis data:", docs)
        for doc in docs:
            Dict = {'taxiName': doc['taxi_reg_no'], 'latitude':doc['currentCoordinates'].get('coordinates')[1],'longitude':doc['currentCoordinates'].get('coordinates')[0]}
            taxi_dict.append(Dict)
        return taxi_dict

    def getTaxiCurrentCoords(self,taxi_reg_no,city):
        taxis = TaxiModel()
        taxidata = taxis.find_taxi_by_reg_no(taxi_reg_no,city)
        print("got data",taxidata)
        docs = list(taxidata)
        taxi_dict = []
        for doc in docs:
            Dict = {'latitude':taxidata['currentCoordinates'].get('coordinates')[1],'longitude':taxidata['currentCoordinates'].get('coordinates')[0]}
            taxi_dict.append(Dict)
        return taxi_dict

    def setInitialTaxiCoords(self,fileToProcess):
        taxiModel = TaxiModel()
        with open(fileToProcess, 'r') as taxis_fh:
            for taxi_row in taxis_fh:
                taxi_row = taxi_row.rstrip()
                if taxi_row:
                    (reg_no, brand, model, type, base_rate, vacant, currentLat, currentLong, city) = taxi_row.split(',')
                taxiModel.insertNewTaxi(reg_no, model, brand, type, vacant, base_rate, currentLat, currentLong)

    def simulateTaxi(self,fileToProcess):
        taxiModel = TaxiModel()
        # At the start - get taxi current location from dB
        # for some 20 taxis keep incrementing the lat long to see some movement.
        # after each increment upsert db and sleep for a second.
        taxiDetails = [] * 30
        i = 0
        with open(fileToProcess, 'r') as taxis_fh:
            for taxi_row in taxis_fh:
                taxi_row = taxi_row.rstrip()
                if taxi_row:
                    (reg_no, brand, model, type, base_rate, vacant, currentLat, currentLong) = taxi_row.split(',')
                taxiDetails.append(taxiModel.find_taxi_by_reg_no(reg_no))
                # i=i+1

        thread_list = []
        for taxi in taxiDetails:
            # creating thread
            thread = threading.Thread(target=self.simulateTaxiMovement, args=(
            taxi["reg_no"], taxi["currentCoordinates"]["coordinates"][0], taxi["currentCoordinates"]["coordinates"][1]))
            thread.start()
            thread_list.append(thread)

        for t in thread_list:
            # wait until thread 1 is completely executed
            t.join()

            print("Done!!")

    def simulateSingleTaxi(self,taxiName,city):
        taxiModel = TaxiModel()
        taxi_data = taxiModel.find_taxi_by_reg_no(taxiName, city)
        self.simulateTaxiMovement(taxiName, city,taxi_data['currentCoordinates']['coordinates'][1], taxi_data['currentCoordinates']['coordinates'][0])

    def simulateTaxiMovement(self,reg_no,city,startLat,startLong):
        taxiModel = TaxiModel()
        currentLat = float(startLat)
        currentLong = float(startLong)
        print(f'Taxi {reg_no} is at {startLat},{startLong}')
        i=1
        while(i<60):
            time.sleep(5)
            currentLat = currentLat + 0.001
            currentLong = currentLong + 0.001
            print(f"Moving Taxi {reg_no} is at [{currentLat}, {currentLong} ]")
            i=i+1
            taxiModel.upsertTaxiCoords(reg_no,city,currentLat,currentLong)

