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
    print(entrada)
    folio = entrada["folio"]
    timeCallLogged = str(datetime.datetime.timestamp(datetime.datetime.now()))
    ddb.put_item(TableName=tableName, 
    Item=
        {'ContactId':{'S':ContactId},
        'event':{'S':'callPlaced'},
        'numeroDestino':{'S':numeroDestino},
        'timeCallLogged':{'S':str(timeCallLogged)},
        'numeroOrigen':{'S':numeroOrigen},
        'mensaje' : {'S':mensaje},
        'folio' : {'S':folio},
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
    
    
    
    
    

