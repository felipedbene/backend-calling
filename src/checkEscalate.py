import boto3
import json
import os
import time
import datetime


def handler(event, context):
    
    body = {"numeroDestino" : "0", "ContactId" : event["ContactId"] }
    print(event)
    callTableName = os.environ["callTableName"]
    escalationTableName = os.environ["escalationTableName"]
    ddb = boto3.client('dynamodb')
    body = dict()
    
    ContactId =  event["ContactId"]
    print(ContactId)
    
    if "LastContactId" in event :
        LastContactId = event["LastContactId"]
        print(LastContactId)
        response = ddb.get_item(TableName=callTableName,Key={ 'ContactId': {"S":str(ContactId)} })
        tiempoAcked = response["Item"]["timeCallAcked"]["S"]
        duration = datetime.datetime.now() - datetime.datetime.fromtimestamp( int(float(tiempoAcked)) )
        duration_in_s = duration.total_seconds()
        duration_in_m = int(divmod(duration_in_s, 60)[0])
        
        print(response)
        print(duration_in_m)
        print(duration_in_s)
        print(duration)
        mensaje = str(response["Item"]["mensaje"]["S"] ).split()
        
        afo = str( response["Item"]["mensaje"]["S"] ).split()[-1]
        proceso = mensaje[-7:-1]
        
        m=str()
        print( proceso )
        
        for p in proceso :
            m = str(m) + " " + str(p)
        
        print( afo )

        if len(response["Item"]) > 0 :
            print("Item mayoer que 0")
            if "timeCierre" not in response["Item"] :
                response = ddb.get_item(TableName=callTableName,Key={ 'ContactId': {"S":str(LastContactId)} })
                print("Cierre no presente")
                numDst = response["Item"]["numeroDestino"]["S"]
                print(numDst)
                consecutivo = ddb.get_item(TableName=escalationTableName,Key= {'NumeroDestino' : {"S": numDst}})
                print(consecutivo)
                if len(consecutivo) > 0 :
                    body = { 'maquina' :  "Tienes una escalación por " + m + afo + " de " + str(duration_in_m) + " minutos de paro" ,
                    'numeroOrigen' : response["Item"]["numeroOrigen"]["S"] , 
                    'numeroDestino' : consecutivo["Item"]["consecutivo"]["S"],
                    'ContactId' : event["ContactId"]
                    }
            else :
                    body = { 'maquina' :  "Escalacion: " + str(response["Item"]["mensaje"]["S"]) ,
                    'numeroOrigen' : response["Item"]["numeroOrigen"]["S"] , 
                    'numeroDestino' : '0',
                    'ContactId' : event["ContactId"]
                    }


    print(body)
    
    return body
    
    
    
    

