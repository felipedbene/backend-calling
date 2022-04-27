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
    request = {'tableName' : tableName}
    try : 
        request["folio"]  = event["queryStringParameters"]["id"]
    except Exception as e :
        request["error"] = str(e)
    finally :

        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table(tableName)
        wasEverAcked = False
        countTries = 0
        contactIds = []
        salida = None
        
        try :
            response = table.query(
                IndexName=indexName,
                KeyConditionExpression=Key('folio').eq(str(request["folio"])))
            print(response)
            if len( response["Items"] ) > 0 :
                
                for item in response["Items"] :
                    countTries +=1
                    contactIds.append(item["ContactId"])
                    if item["acked"] == "yes" :
                        
                        salida = { "acked" : "yes",
                        "countTries" : str(countTries),
                        "mensaje" : str( item["mensaje"] ),
                        "timeCallAcked" : str( item["timeCallAcked"] ),
                        "timeCallLogged" : str(item["timeCallLogged"]),
                        "ContactId" : item["ContactId"],
                        "estatus" : "CALL_ACKED"
                        }
                        
                        
                        if "timeLlegado" in item :
                            salida["timeLlegado"] = item["timeLlegado"]
                            salida["estatus"] = "HAS_ARRIVED"
                            
                        if "timeCierre" in item :
                            salida["estatus"] = "CALL_CLOSED"
                            salida["timeCierre"] = item["timeCierre"]
                            
                            
                if salida is None :
                    salida = { "acked" : "no",
                        "countTries" : str(countTries),
                        "mensaje" : str( item["mensaje"] ),
                        "timeCallLogged" : str(item["timeCallLogged"]),
                        "contactIds" : contactIds,
                        "estatus" : "CALL_NOT_ACKED"
                        }
            else :
                print("Menor que 0")
                print(response["Items"])
                salida = { 
                "acked" : "no",
                "estatus" : "NO_CONTACT_IDS"
                }

            
        except Exception as e :
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            salida = str(e)
            
        
        
        
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Headers': '*',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': '*'
            },
            'body': json.dumps(salida)
        }
    
    
    

