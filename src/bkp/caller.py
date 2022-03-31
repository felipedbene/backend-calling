import boto3
import json
import os
import time
import datetime


def handler(event, context):
    tableName = os.environ["tableName"]
    ddb = boto3.client('dynamodb')
    body = dict()

    ContactId = event["ContactId"]
    numeroDestino = event["numeroDestino"]
    mensaje = event["mensaje"]
    timeCallLogged = datetime.datetime.timestamp(datetime.datetime.now())*1000
    ddb.put_item(TableName=tableName, 
    Item=
        {'ContactId':{'S':ContactId},
        'event':{'S':'callPlaced'},
        'numeroDestino':{'S':numeroDestino},
        'timeCallLogged':{'N':timeCallLogged},
        'acked':{'S':'no'}
        } 
    )


    
    body = event
        
    
    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST'
        },
        'body': json.dumps(body)
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
    
    
    
    
    

