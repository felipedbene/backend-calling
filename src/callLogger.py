import boto3
import json
import os
import time
import datetime


def handler(event, context):
    tableName = os.environ["tableName"]
    ddb = boto3.client('dynamodb')
    body = dict()
    entrada = json.loads(event["body"])
    ContactId = entrada["ContactId"]
    numeroDestino = entrada["numeroDestino"]
    numeroOrigen = entrada["numeroOrigen"]
    mensaje = entrada["mensaje"]
    timeCallLogged = datetime.datetime.timestamp(datetime.datetime.now())*1000
    ddb.put_item(TableName=tableName, 
    Item=
        {'ContactId':{'S':ContactId},
        'event':{'S':'callPlaced'},
        'numeroDestino':{'S':numeroDestino},
        'timeCallLogged':{'N':str(timeCallLogged)},
        'numeroOrigen':{'S':numeroOrigen},
        'mensaje' : {'S':mensaje}, 
        'acked':{'S':'no'}
        } 
    )


    
    body = event["body"]
        
    
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
    
    
    
    
    

