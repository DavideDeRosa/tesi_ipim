import json
import boto3

client = boto3.client('dynamodb')
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table('product-inventory')
tableName = 'product-inventory'

def lambda_handler(event, context):
    print(event)

    body = {}
    statusCode = 200

    try:
        body = table.get_item(Key={'id': event['pathParameters']['id']})
        body = body["Item"]
        responseBody = [{'price': body['price'], 'id': body['id'], 'name': body['name'], 'description': body['description']}]
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