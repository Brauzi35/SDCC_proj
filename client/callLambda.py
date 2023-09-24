import boto3
import json

def startLambda(number, function_name):
    # Crea un client Lambda
    lambda_client = boto3.client('lambda', region_name='us-east-1')  # Sostituisci con la tua regione AWS

    # Definisci i parametri per l'invocazione della funzione Lambda
    #function_name = 'FactorialLambda'
    #function_name = 'FactorizeLambda'
    payload = {
        'number': number  # Sostituisci con il numero da cercare nel CSV
    }
    # Invoca la funzione Lambda
    response = lambda_client.invoke(
        FunctionName=function_name,
        InvocationType='RequestResponse',
        Payload=json.dumps(payload)
    )

    # Estrai la risposta
    response_payload = response['Payload'].read()
    return response_payload
    print(response_payload)
