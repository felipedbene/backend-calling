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
    
    
    extractedBody = json.loads(json.loads(event["body"]))
    print(extractedBody)
    ContactId = extractedBody['ContactId']
    print(ContactId)
    response = ddb.get_item(TableName=tableName,Key={ 'ContactId': {"S":str(ContactId)} },AttributesToGet=['acked'])
    print(response)
    if len(response["Item"]) > 0 :
        body["acked"] = response["Item"]["acked"]["S"]
        body["ContactId"] = ContactId
        body["isFirstCall"] = "no"
        body["folio"] = extractedBody["folio"]
    
    return body

    
    
    
    
    

