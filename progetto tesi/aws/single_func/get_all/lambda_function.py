import json
import boto3

client = boto3.client('dynamodb')
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table('product-inventory')

def lambda_handler(event, context):
    body = {}
    statusCode = 200

    try:
        body = table.scan()
        body = body["Items"]
        responseBody = []
        for items in body:
            responseItems = [{'price': items['price'], 'id': items['id'], 'name': items['name'], 'description': items['description']}]
            responseBody.append(responseItems)
        body = responseBody
    except KeyError:
        statusCode = 400
        body = 'Unsupported route: ' + event['routeKey']
    
    body = json.dumps(body)
    res = {
        "statusCode": statusCode,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": body
    }

    return res