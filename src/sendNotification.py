from pprint import pprint
import boto3
import json
import csv
import datetime
import os
import random
import base64

class SendNotifications:

    def __init__(self):
        self.client = boto3.client('sns', region_name='us-east-1')
        self.topic_arn = "arn:aws:sns:us-east-1:160643791587:StockPricePOIMessages"

    def sendNotification(self, message,subject):
        result = 0
        print(f'trying to send notification to SNS ')
        try:
            self.client.publish(TopicArn=self.topic_arn,
                                Message=message,
                                Subject=subject)
            result = 1
        except Exception:
            print(f'Exception occured while sending SNS')
            result = 0
        return result

