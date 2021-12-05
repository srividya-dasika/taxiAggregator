from src.Taxi.taxiModel import TaxiModel #WeatherDataModel, DeviceAccessModel,DailyReportModel
from src.Users.userModel import UserModel
from datetime import datetime

user_coll = UserModel()
taxi_coll = TaxiModel()

user_coll.insertNewUser("test123","test@test.com","2021-10-10","male",1234123412,"test",10.1234,12.1234)

taxi_coll.insertNewTaxi("ka12bs1234","Test","Test23","economy","true",30,12.1234,12.2334)
