from pprint import pprint
import boto3
import json
import csv
import datetime
import os
import random
import base64

class SendNotifications:

    DRIVER_ARN="arn:aws:sns:us-east-1:160643791587:driverTopic"
    USER_ARN="arn:aws:sns:us-east-1:160643791587:userTopic"

    def __init__(self):
        configFile = open("Config.txt", "r")
        for line in configFile.readlines():
            x = line.split("=")
            if x[0] == "driver_arn":
                self.DRIVER_ARN = x[1][:-1]
            if x[0] == "user_arn":
                self.USER_ARN = x[1][:-1]
        self.client = boto3.client('sns', region_name='us-east-1')
        #self.topic_arn = "arn:aws:sns:us-east-1:160643791587:StockPricePOIMessages"
        #self.driver_arn="arn:aws:sns:us-east-1:160643791587:driverTopic"
        #self.user_arn = "arn:aws:sns:us-east-1:160643791587:userTopic"

    def sendNotification(self, message,subject,type):
        result = 0
        print(f'trying to send notification to SNS ')
        if type == 'driver':
            arn = self.DRIVER_ARN
        elif type == 'user':
            arn = self.USER_ARN
        try:
            self.client.publish(TopicArn=arn,
                                    Message=message,
                                    Subject=subject)
            result = 1
        except Exception:
            print(f'Exception occured while sending SNS')
            result = 0
        return result

