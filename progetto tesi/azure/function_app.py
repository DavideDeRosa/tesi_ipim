import azure.functions as func
import logging
import json
from azure.cosmos import CosmosClient, PartitionKey

# Initialize the Cosmos client
endpoint = "your_cosmos_db_endpoint"
key = "your_cosmos_db_key"
client = CosmosClient(endpoint, key)

database_name = 'product-inventory-db'
container_name = 'product-inventory'

# Retrieve the database and container
database = client.get_database_client(database_name)
container = database.get_container_client(container_name)

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

@app.route(route="health")
def health_check(req: func.HttpRequest) -> func.HttpResponse:
    return func.HttpResponse("Health check!", status_code=200)

@app.route(route="items/{id}", methods=["GET"])
def get_item(req: func.HttpRequest, id: str) -> func.HttpResponse:
    try:
        item = container.read_item(item=id, partition_key=id)
        response_body = {
            'price': item['price'],
            'id': item['id'],
            'name': item['name'],
            'description': item['description']
        }
        return func.HttpResponse(json.dumps(response_body), status_code=200, mimetype="application/json")
    except Exception as e:
        logging.error(f"Error getting item: {str(e)}")
        return func.HttpResponse(f"Item not found: {id}", status_code=404)

@app.route(route="items", methods=["GET"])
def list_items(req: func.HttpRequest) -> func.HttpResponse:
    try:
        items = container.read_all_items()
        response_body = []
        for item in items:
            response_body.append({
                'price': item['price'],
                'id': item['id'],
                'name': item['name'],
                'description': item['description']
            })
        return func.HttpResponse(json.dumps(response_body), status_code=200, mimetype="application/json")
    except Exception as e:
        logging.error(f"Error listing items: {str(e)}")
        return func.HttpResponse(f"Error listing items", status_code=500)

@app.route(route="items/{id}", methods=["DELETE"])
def delete_item(req: func.HttpRequest, id: str) -> func.HttpResponse:
    try:
        container.delete_item(item=id, partition_key=id)
        return func.HttpResponse(f"Deleted item {id}", status_code=200)
    except Exception as e:
        logging.error(f"Error deleting item: {str(e)}")
        return func.HttpResponse(f"Error deleting item: {id}", status_code=500)

@app.route(route="items", methods=["PUT"])
def put_item(req: func.HttpRequest) -> func.HttpResponse:
    try:
        request_json = req.get_json()
        container.upsert_item({
            'id': request_json['id'],
            'price': request_json['price'],
            'name': request_json['name'],
            'description': request_json['description']
        })
        return func.HttpResponse(f"Put item {request_json['id']}", status_code=200)
    except Exception as e:
        logging.error(f"Error putting item: {str(e)}")
        return func.HttpResponse(f"Error putting item", status_code=500)