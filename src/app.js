const AWS = require('aws-sdk');
var connect = new AWS.Connect();
let response;
// main entry to the flow
// arn:aws:connect:us-east-1:668984504585:instance/40f62289-8adf-4f1a-b934-328736bd08de/contact-flow/11e0d624-6809-4e7d-8fa4-cd18e6238773
// arn:aws:connect:us-east-1:668984504585:instance/40f62289-8adf-4f1a-b934-328736bd08de/queue/32f87844-f47f-4d7f-91c9-53dfc308e152

exports.handler = async (event, context) => {
    try {
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
                console.log(maquina);
            }
        }
        
    
               console.log(maquina);
        
        console.log(`---- Starting the phone call for ${maquina} ---- `);
        
        var params = {
            ContactFlowId: "11e0d624-6809-4e7d-8fa4-cd18e6238773",
            DestinationPhoneNumber: numeroDestino,
            InstanceId: "40f62289-8adf-4f1a-b934-328736bd08de",
//            QueueId: "32f87844-f47f-4d7f-91c9-53dfc308e152",
            Attributes: {"NombreMaquina": maquina }, // $.Attributes.NombreMaquina
            SourcePhoneNumber: numeroOrigen
        };
    
        console.log(`Debug params : ${params}`)
        // method used to initiate the outbound call from Amazon Connect
        connect.startOutboundVoiceContact(params, function(err, data) {
            if (err) console.log(err, err.stack) ;
            else console.log(data);
        });
    
        response = {
            statusCode: 200,
            body: JSON.stringify("ok")
        };
        console.log("response: " + JSON.stringify(response))
    } catch (err){
        console.log(err);
        return err;
    }
    
    return response;
};