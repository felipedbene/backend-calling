import json
import requests
from requests_aws4auth import AWS4Auth
import boto3
from boto3.dynamodb.conditions import Key, Attr
import datetime
import os

def selectSpec(area):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('specialists')
    response = table.query(
    IndexName="specialty-lastAssignment-index",
    KeyConditionExpression=Key('specialty').eq(area))
    if len(response["Items"]) > 0 :
        spec = response["Items"][0]["alias"]
    else :
        spec = ""
    print("Assign to :{}".format(spec))
    return spec

def updateStats(alias,specialty) :
    ahora = datetime.datetime.now().isoformat()
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('specialists')
    try :
        response = table.update_item(Key={"alias":alias, "specialty": specialty },
        AttributeUpdates={'lastAssignment': {'Value': ahora }}
        )
        print("Updated assignment time for {}".format(alias))
    except :
        print("Error updating stats")
    
def simrequest(method,ticket,body=""):
    auth = AWS4Auth(os.environ.get('access_key') ,os.environ.get('secret_key') ,'us-east-1','sim')
    headers= {'User-Agent' : 'Robot v0.1'}
    
    if method == "get" :
        response = requests.get('https://issues-ext.amazon.com/issues/{}'.format(ticket),
                                  auth=auth, headers=headers)
        return response.json()
    if method == "post" :
        print(body)
        headers= {'User-Agent' : 'Robot v0.1','Content-Type':'application/json;charset=utf-8'}
        response = requests.post('https://issues-ext.amazon.com/issues/{}/edits'.format(ticket),
                                  auth=auth, headers=headers, data=json.dumps(body))
        

def get_ticket_info(ticket):
    response = simrequest("get",ticket)
    return response

    
def assignTktTo(ticketNumber,assignee) :
    body={"pathEdits":[{"path":"/assigneeIdentity","editAction":"PUT","data":"kerberos:benfelip@ANT.AMAZON.COM"}]}
    body["pathEdits"][0]["data"] = "kerberos:{}@ANT.AMAZON.COM".format(assignee)
    #print("Assigned to {}".format(body["pathEdits"][0]["data"]))
    simrequest("post",ticketNumber,body)

def selectPSA(area):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Partner_PSA')
    response = table.query(
    IndexName="partner-lastAssignment-index",
    KeyConditionExpression=Key('partner').eq(area))
    if len(response["Items"]) > 0 :
        spec = response["Items"][0]["psa"]
    else :
        spec = ""
    print("Assign to PSA Team :{}".format(spec))
    return spec   

def updatePSAStats(alias, partner):
    ahora = datetime.datetime.now().isoformat()
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Partner_PSA')
    try :
        response = table.update_item(Key={"partner":partner, "psa": alias },
        AttributeUpdates={'lastAssignment': {'Value': ahora }}
        )
        print("Updated assignment time for {}".format(alias))
    except :
        print("Error updating stats for PSA")    
    
def lambda_handler(event, context):
    
    #Need to getTicket number from the event
    #print(event) <- Event Shape
    #Some Boring Json parsing
    notificationDict = json.loads(event["Records"][0]["body"])
    
    message=json.loads(notificationDict["Message"])
    if message["action"] == "Create" :
        ticketNumber=message["documentId"]["id"]
        
        #Get the ticket classification field
        tktDict = get_ticket_info(ticketNumber)
        

            
        print(tktDict["customFields"]["string"])
        #Dispatch(Assign) and die
        print(tktDict["customFields"]["string"][5])
        
        area = ""
        for item in tktDict["customFields"]["string"]:
            if item["id"] == "technical_area" :
                area = item["value"]
                
        for item in tktDict["customFields"]["string"]:
            if item["id"] == "partner" :
                partner = item["value"]
        
        #Validate custom fields existence
        if area != "" :
            alias = selectSpec(area)
            updateStats(alias, area)
            
            if alias == "PSA":
                alias = selectPSA(partner)
                
                if alias == "" :
                    alias = selectSpec(area)
                else :
                    updatePSAStats(alias, partner)
                
            if alias != "" :
                assignTktTo(ticketNumber,alias)
            else :
                print("No PSAs or SAs could be assigned")
            
                
        return {
            'statusCode': 200,
            'body': 'Done!'
        }