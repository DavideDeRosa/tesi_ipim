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
        if path.startswith("/items/") and method == "DELETE":
            item_id = path.split('/')[-1]
            doc_ref = client.collection(collection_name).document(item_id)
            doc_ref.delete()
            body = f'Deleted item {item_id}'
        elif path.startswith("/items/") and method == "GET":
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
        elif path == "/items" and method == "GET":
            docs = client.collection(collection_name).stream()
            responseBody = []
            for doc in docs:
                doc_dict = doc.to_dict()
                responseItems = [{'price': doc_dict['price'], 'id': doc.id, 'name': doc_dict['name'], 'description': doc_dict['description']}]
                responseBody.append(responseItems)
            body = responseBody
        elif path == "/items" and method == "PUT":
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