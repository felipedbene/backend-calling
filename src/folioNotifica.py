import boto3
import json
import os
import time
import datetime
from boto3.dynamodb.conditions import Key


def handler(event, context):
    
    print(event)
    tableName = os.environ["tableName"]
    escalationMachineARN = os.environ["escalationMachine"]
    request = dict()
    
    try : 
        request["ContactId"]  = event["queryStringParameters"]["ContactId"]
    except Exception as e :
        request["error"] = str(e)
        
    finally :
        
        ddb = boto3.client('dynamodb')
        timeLlegada = str(datetime.datetime.timestamp(datetime.datetime.now()))
        
        escalationMachine = boto3.client('stepfunctions')

        try :
            response = ddb.update_item(Key={ 'ContactId': {"S":str(request["ContactId"])} },
            AttributeUpdates={'hallegado': {'Value': {'S' :'yes'} }, 'timeLlegada' :  {'Value' : { 'S' : timeLlegada }} },
            TableName=tableName)

            resp = {'ContactId'  : request["ContactId"] ,
            'status' : 'ok',
            'LastContactId' : request["ContactId"]
            }
            
            responseSM = escalationMachine.start_execution(
                stateMachineArn=escalationMachineARN,
                name=str(request["ContactId"]),
                input=str(json.dumps(resp))
                )

            
        except Exception as e :
            print(e)
            response = str(e)
        
        
        
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Headers': '*',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': '*'
            },
            'body': json.dumps(resp)
        }
    
    
    

