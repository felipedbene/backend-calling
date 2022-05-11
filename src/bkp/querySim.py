import json
import requests
from requests_aws4auth import AWS4Auth
import boto3
import datetime
import os
import csv




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

def getCustomField(tipo,fields,field_name):
    if tipo in fields.keys() :
        for i in fields[tipo] :
            if i['id'] == field_name :
                if tipo == "string" or tipo == "date": 
                    return i['value']
                elif tipo == "checkbox" :
                    for j in i['value'] :
                        if j['checked'] == True :
                            return j['value']
        
    else:
        return ""

if __name__ == "__main__" :
    folder = "6caffcac-8986-4a53-9477-adca9d7aab5c"
    response = simrequest("get","?q=containingFolder:" + folder)
    #print(response)
    
    with open('simTkts.csv','w',newline='') as csvfile :
        fieldnames = ['title','assigneeIdentity','requesterIdentity','createDate','ticket_id','client_name','opportunity_if_applicable','estimated_effort','technical_area','partner','engagement_type','required_date','no_partner_reason']
        writer = csv.DictWriter(csvfile,fieldnames=fieldnames,delimiter='|',quotechar='|')
        writer.writeheader()
        docDict = {}
        for doc in response["documents"] :
            
            docDict['title'] = doc['title']
            #
            # Assignee can be null, therefore we have to manually treat that case
            #
            try :
                docDict['assigneeIdentity'] = doc['assigneeIdentity']
            except KeyError :
                docDict['assigneeIdentity'] = 'nobody'
                
            docDict['requesterIdentity'] = doc['requesterIdentity']
            docDict['createDate'] = doc['createDate']
            docDict['ticket_id'] = doc['id']
            
            #
            # Custom field extraction
            # These multi-nested field so it's necessary to write a function specific for this
            #
            
            docDict['client_name'] = getCustomField("string", doc["customFields"] ,"client_name")
            docDict['opportunity_if_applicable'] = getCustomField("string", doc["customFields"] ,"opportunity_if_applicable")
            docDict['estimated_effort'] = getCustomField("string",doc["customFields"] ,"estimated_effort")
            docDict['technical_area'] = getCustomField("string",doc["customFields"] ,"technical_area")
            docDict['partner'] = getCustomField("string",doc["customFields"] ,"partner")
            docDict['engagement_type'] = getCustomField("checkbox",doc["customFields"] ,"engagement_type")
            docDict['required_date'] =getCustomField("date",doc["customFields"] ,"required_date")
            docDict['no_partner_reason'] = getCustomField("checkbox",doc["customFields"] ,"no_partner_reason")
            #print(docDict['required_date'])
            
            writer.writerow(docDict)
    csvfile.close()
 