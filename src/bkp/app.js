const AWS = require('aws-sdk');

// main entry to the flow
// arn:aws:connect:us-east-1:668984504585:instance/40f62289-8adf-4f1a-b934-328736bd08de/contact-flow/11e0d624-6809-4e7d-8fa4-cd18e6238773
// arn:aws:connect:us-east-1:668984504585:instance/40f62289-8adf-4f1a-b934-328736bd08de/queue/32f87844-f47f-4d7f-91c9-53dfc308e152

exports.handler = (event, context) => {
    //context.callbackWaitsForEmptyEventLoop = false;
    const connect = new AWS.Connect();
    let response;
    let res;
    //try {
        console.log(event);
        //define parameter values to use in initiating the outbound call
        let maquina = "";
        let numeroOrigen = "";
        let numeroDestino = "";
        
        if (event.body) { 
            
            let body = JSON.parse(event.body);
            
            if (body.maquina && body.numeroDestino && body.numeroOrigen) {
                maquina = body.maquina;
                numeroOrigen = body.numeroOrigen;
                numeroDestino = body.numeroDestino;
                console.log("Parsed JSON");
            }
        }
        
    

        
        console.log(`---- Starting the phone call for message :  ${maquina} ---- `);
        
        var params = {
            ContactFlowId: "11e0d624-6809-4e7d-8fa4-cd18e6238773",
            DestinationPhoneNumber: numeroDestino,
            InstanceId: "40f62289-8adf-4f1a-b934-328736bd08de",
//            QueueId: "32f87844-f47f-4d7f-91c9-53dfc308e152",
            Attributes: {"NombreMaquina": maquina }, // $.Attributes.NombreMaquina
            SourcePhoneNumber: numeroOrigen
        };
    
        console.log(`Debug params : ${params.DestinationPhoneNumber}`)
        // method used to initiate the outbound call from Amazon Connect
        connect.startOutboundVoiceContact(params, function(err, data) {
            if (err) {
                console.log("pasó un error!");
                console.log(err, err.stack);
                
            } 
            else{ 
                console.log("Mande la llamada a connect, sigue data:");
                return data;
            };
        });
        
    
        response = {
            statusCode: 200,
            headers: {
            "Access-Control-Allow-Headers" : "Content-Type,access-control-allow-credentials,access-control-allow-headers,access-control-allow-methods,access-control-allow-origin,content-type,x-requested-with",
            "Access-Control-Allow-Origin": "*", // Allow from anywhere 
            "Access-Control-Allow-Methods": "OPTIONS,POST" // Allow only GET request 
        },
            body: JSON.stringify("ok")
        };
        console.log("response: " + JSON.stringify(response))
//    } catch (err){
//        console.log(err);
//       return err;
//   }
    
    return response;
};