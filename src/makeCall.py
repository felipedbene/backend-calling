import boto3
import json
import os

def checkCallLog(ContactId):
    ddb = boto3.client('dynamodb')
    tableName = os.environ["tableName"]
    response = ddb.get_item(TableName=tableName,Key={ 'ContactId': {"S":str(ContactId)} },AttributesToGet=['numeroDestino','numeroOrigen','mensaje','folio'])
    inputDic = {}
    if len(response["Item"]) > 0 :
        inputDic["maquina"] = response["Item"]["mensaje"]["S"]
        inputDic["numeroOrigen"] = response["Item"]["numeroOrigen"]["S"]
        inputDic["numeroDestino"] = response["Item"]["numeroDestino"]["S"]
        inputDic["folio"] = response["Item"]["folio"]["S"]
    return inputDic

def handler(event, context):
    print("Event"+ str(event))
    client = boto3.client('connect')

    try :
        print("Assumiendo APIGateway Event, tratando event como dict y json encapsulado en una string body")
        inputDic = json.loads(event["body"])
    except TypeError:
        print("Exception Step Function Event, tratando event como dict con mis atributos cargados")
        print(str(event))
        inputDic = event["body"]
    except KeyError:
        #Si es una segunda llamada en body no existe, luego key error
        ContactId = str(event["ContactId"])
        print("Contact ID:" + ContactId)
        inputDic = checkCallLog(ContactId)
        inputDic["isFirstCall"] = "no"
    
    print(inputDic["maquina"])
    print(inputDic["numeroOrigen"])
    print(inputDic["numeroDestino"])
    print(inputDic["isFirstCall"])
    body = dict()

    try : 
        response = client.start_outbound_voice_contact(
            DestinationPhoneNumber=str(inputDic["numeroDestino"]),
            ContactFlowId='11e0d624-6809-4e7d-8fa4-cd18e6238773',
            InstanceId='40f62289-8adf-4f1a-b934-328736bd08de',
            SourcePhoneNumber=str(inputDic["numeroOrigen"]),
            Attributes={
                'NombreMaquina': str(inputDic["maquina"])
            }
            )

            
        print("Contact id : " + str(response["ContactId"]))
        body["ContactId"] = str(response["ContactId"])
        body["status"] = "ok"
        body["numeroDestino"] = inputDic["numeroDestino"]
        body["numeroOrigen"] = inputDic["numeroOrigen"]
        body["mensaje"] = inputDic["maquina"]
        body["folio"] = inputDic["folio"]
        
        if inputDic["isFirstCall"] == 'yes' :  
            body["needFUP"] = "yes"
        else :
            body["needFUP"] = "no"
            
        
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,POST'
            },
            'body': json.dumps(body)
        }
    except :
        body["status"] = "kaput"
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,POST'
            },
            'body': json.dumps(body)
        }
    
    
    
    
    

