import boto3
import json
import os
import time
import datetime


def handler(event, context):
    print(event)
    tableName = os.environ["tableName"]
    ddb = boto3.client('dynamodb')
    body = dict()
    ContactId = event["Details"]["ContactData"]["ContactId"]
    
    print(ContactId)
    
    timeCallAcked = datetime.datetime.timestamp(datetime.datetime.now())*1000

    cont = dict()
    cont["ContactId"]=ContactId
    response = ddb.update_item(Key={ 'ContactId': {"S":str(ContactId)} },
    AttributeUpdates={'acked': {'Value': {'S' :'yes'} }},
    TableName=tableName)


    
    body = event["Details"]["ContactData"]["ContactId"]
        
    
    return {
        'ContactId': body
    }
    # except :
    #     body["status"] = "kaput"
    #     return {
    #         'statusCode': 500,
    #         'headers': {
    #             'Access-Control-Allow-Headers': 'Content-Type',
    #             'Access-Control-Allow-Origin': '*',
    #             'Access-Control-Allow-Methods': 'OPTIONS,POST'
    #         },
    #         'body': json.dumps(body)
    #     }
    
    
    
    
    

