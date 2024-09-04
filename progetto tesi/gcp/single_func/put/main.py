import json
from google.cloud import firestore

client = firestore.Client()
collection_name = 'ProductInventory'

def function(request):
    request_json = request.get_json(silent=True)
    path = request.path
    method = request.method

    body = {}
    statusCode = 200

    try:
        if path == "/items" and method == "PUT":
            if not request_json:
                raise ValueError("No request body")
            item_id = request_json['id']
            doc_ref = client.collection(collection_name).document(item_id)
            doc_ref.set({
                'price': request_json['price'],
                'name': request_json['name'],
                'description': request_json['description']
            })
            body = f'Put item {item_id}'
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