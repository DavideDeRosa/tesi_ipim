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
        if path.startswith("/items/") and method == "GET":
            item_id = path.split('/')[-1]
            doc_ref = client.collection(collection_name).document(item_id)
            doc = doc_ref.get()
            if doc.exists:
                doc_dict = doc.to_dict()
                responseBody = [{'price': doc_dict['price'], 'id': doc.id, 'name': doc_dict['name'], 'description': doc_dict['description']}]
                body = responseBody
            else:
                statusCode = 404
                body = f'Item with id {item_id} not found'
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