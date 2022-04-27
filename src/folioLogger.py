import boto3
import json
import os
import time
import datetime


def handler(event, context):
    
    tableName = os.environ["tableName"]
    ddb = boto3.client('dynamodb')
    body = dict()

    print(event)
    
    time1stFlowEnded = str(datetime.datetime.timestamp(datetime.datetime.now()))
    ContactId = event["ContactId"]
    print(ContactId)
    try :
        response = ddb.update_item(Key={ 'ContactId': {"S":str(ContactId)} },
        AttributeUpdates={
            'time1stFlowEnded' : {'Value' : { 'S': str(time1stFlowEnded)} }
        },
        TableName=tableName)
        
        body = {
            'ContactId': ContactId,
            'folio' : event['folio'],
            'isFirstCall' : event['isFirstCall'],
            'acked' : event['acked']
        }
        return {
        'statusCode': 200,
        'body': json.dumps(body)
        }
    except Exception as e:
        print(e)
        return {
        'statusCode': 500,
        'body': str(e)
        }
    
    

