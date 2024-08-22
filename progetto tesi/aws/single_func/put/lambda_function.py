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
        requestJSON = json.loads(event['body'])
        table.put_item(
            Item={
                'id': requestJSON['id'],
                'price': requestJSON['price'],
                'name': requestJSON['name'],
                'description': requestJSON['description']
            })
        body = 'Put item ' + requestJSON['id']
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