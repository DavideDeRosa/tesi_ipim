import json
from google.cloud import firestore

client = firestore.Client()
collection_name = 'ProductInventory'

def function(request):
    path = request.path
    method = request.method

    body = {}
    statusCode = 200

    try:
        if path == "/items" and method == "GET":
            docs = client.collection(collection_name).stream()
            responseBody = []
            for doc in docs:
                doc_dict = doc.to_dict()
                responseItems = [{'price': doc_dict['price'], 'id': doc.id, 'name': doc_dict['name'], 'description': doc_dict['description']}]
                responseBody.append(responseItems)
                body = responseBody
        else:
            raise KeyError(f'Unsupported route: {method} {path}')
    except KeyError as e:
        statusCode = 400
        body = str(e)
    except Exception as e:
        statusCode = 500
        body = str(e)
    
    res = {
        "statusCode": statusCode,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps(body)
    }

    return (res["body"], res["statusCode"], res["headers"])