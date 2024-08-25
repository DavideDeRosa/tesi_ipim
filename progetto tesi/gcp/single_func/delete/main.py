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
        if path.startswith("/items/") and method == "DELETE":
            item_id = path.split('/')[-1]
            doc_ref = client.collection(collection_name).document(item_id)
            doc_ref.delete()
            body = f'Deleted item {item_id}'
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