import time

import pandas as pd
import threading
from taxiModel import TaxiModel

class TaxiSimulator:

    def processdata(self,fileToProcess):
        # Loading and reading the CSV file.
        df = pd.read_csv(fileToProcess, delimiter =',')
        # Converting the CSV data to a list.
        df = df.to_dict(orient = 'records')
        return df


    def setInitialTaxiCoords(self,fileToProcess):
        taxiModel = TaxiModel()
        with open(fileToProcess, 'r') as taxis_fh:
            for taxi_row in taxis_fh:
                taxi_row = taxi_row.rstrip()
                if taxi_row:
                    (reg_no, brand, model, type, base_rate, vacant, currentLat, currentLong, city) = taxi_row.split(',')
                    #print(reg_no, brand, model, type, base_rate, vacant, currentLat, currentLong, city)
                taxiModel.insertNewTaxi(reg_no, model, brand, type, vacant, base_rate, currentLat, currentLong, city)

    def simulateTaxis(self,fileToProcess):
        taxiModel = TaxiModel()
        #At the start - get taxi current location from dB
        #for some 20 taxis keep incrementing the lat long to see some movement.
        #after each increment upsert db and sleep for a second.
        taxiDetails= []*30
        i=0
        with open(fileToProcess, 'r') as taxis_fh:
            for taxi_row in taxis_fh:
                taxi_row = taxi_row.rstrip()
                if taxi_row:
                    (reg_no, brand, model, type, base_rate, vacant, currentLat, currentLong) = taxi_row.split(',')
                taxiDetails.append(taxiModel.find_taxi_by_reg_no(reg_no))
                #i=i+1

        thread_list = []
        for taxi in taxiDetails:
            # creating thread
            thread = threading.Thread(target=self.simulateTaxiMovement, args=(taxi["reg_no"],taxi["currentCoordinates"]["coordinates"][0],taxi["currentCoordinates"]["coordinates"][1]))
            thread.start()
            thread_list.append(thread)

        for t in thread_list:
            # wait until thread 1 is completely executed
            t.join()

            print("Done!!")

    def simulateTaxiMovement(self,reg_no,startLat,startLong):
        taxiModel = TaxiModel()
        currentLat = float(startLat)
        currentLong = float(startLong)
        print("Taxi "+reg_no+" is at ["+startLat+","+startLong+"]")
        i=1
        while(i<10):
            time.sleep(1)
            currentLat = currentLat + 0.001
            currentLong = currentLong + 0.001
            print(f"Moving Taxi {reg_no} is at [{currentLat}, {currentLong} ]")
            i=i+1
           # taxiModel.upsertTaxiCoords(taxiDetails.split('&')[0], taxiDetails.split('&')[1], taxiDetails.split('&')[2])

