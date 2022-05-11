import boto3
import json
import os
import time
import datetime


def handler(event, context):
    tableName = os.environ["tableName"]
    ddb = boto3.client('dynamodb')

    print("Event"+ str(event))
    client = boto3.client('connect')
    
    
    print(event["maquina"])
    print(event["numeroOrigen"])
    print(event["numeroDestino"])
    
    body = dict()

    
    response = client.start_outbound_voice_contact(
        DestinationPhoneNumber=str(event["numeroDestino"]),
        ContactFlowId='2c2ceae2-b88b-40bd-a739-2fcba7e4c2a0',
        InstanceId='40f62289-8adf-4f1a-b934-328736bd08de',
        SourcePhoneNumber=str(event["numeroOrigen"]),
        Attributes={
            'NombreMaquina': str(event["maquina"])
        }
        )
    LastContactId = response["ContactId"]
    
    ContactId = event["ContactId"]
    
    timeCallLogged = str(datetime.datetime.timestamp(datetime.datetime.now()))
    
    ddb.put_item(TableName=tableName, 
    Item=
        {'ContactId':{'S':LastContactId},
        'event':{'S':'escalationMachine'},
        'numeroDestino':{'S':event["numeroDestino"]},
        'timeCallLogged':{'S':str(timeCallLogged)},
        'numeroOrigen':{'S':event["numeroOrigen"]},
        'mensaje' : {'S':event["maquina"]}
        } 
    )
    return  {"ContactId": event["ContactId"],
    "numeroOrigen" : event["numeroOrigen"],
    "numeroDestino"  : event["numeroDestino"],
    "maquina" : event["maquina"],
    "LastContactId" : LastContactId
    }

    
    
    
    

