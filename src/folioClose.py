import boto3
import json
import os
import sys
import time
import datetime
from boto3.dynamodb.conditions import Key, Attr


def handler(event, context):
    print(event)
    
    tableName = os.environ["tableName"]
    indexName = os.environ["indexName"]
    request = dict()
    

            
        
    try :
#        'body': '{"turno":"","ccCargo":"23123","descripcionFalla":"123123","reparador":"132131","trabajoEjecutado":"3123123","ContactId":"7f19ec09-ea70-4c2c-b9bf-4fa934246272"}
        body = json.loads(event["body"])
        print(body)
        body["status"] = "ok"
        response = body
        
        ddb = boto3.client('dynamodb')
        timeCierre = str(datetime.datetime.timestamp(datetime.datetime.now()))
        response = ddb.update_item(Key={ 'ContactId': {"S":str(body["ContactId"])} },
        AttributeUpdates={'timeCierre': {'Value': {'S' :timeCierre} }, 
        'turno' :  {'Value' : { 'S' : body["turno-radio"] }},
        'ccCargo' : {'Value' : { 'S' : body["ccCargo"] }},
        'descripcionFalla' : {'Value' : { 'S' : body["descripcionFalla"] }},
        'reparador' : {'Value' : { 'S' : body["reparador"] }},
        'trabajoEjecutado' : {'Value' : { 'S' : body["trabajoEjecutado"] }}
        },
        TableName=tableName)
        
        response = {'ContactId'  : body["ContactId"] ,
            'status' : 'ok'
        }

    except Exception as e:
        print(e)
        response = e
        
    return {
    'statusCode': 200,
    'headers': {
        'Access-Control-Allow-Headers': '*',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': '*'
    },
    'body': json.dumps(response)
    }