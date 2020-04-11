import boto3
import json
from botocore.vendored import requests
from aws_requests_auth.aws_auth import AWSRequestsAuth

print('Loading function')
dynamo = boto3.client('dynamodb')

session = boto3.session.Session()
credentials = session.get_credentials()
es_host = 'search-nyc-restaurants-inspection-oksmivk4fqfcwxeprrwjvp32ii.us-east-1.es.amazonaws.com'
aws_auth = AWSRequestsAuth(
    aws_access_key=credentials.access_key,
    aws_secret_access_key=credentials.secret_key,
    aws_token=credentials.token,
    aws_host=es_host,
    aws_region=session.region_name,
    aws_service='es'
)
# access ES example
"""
req = requests.get('https://search-nyc-restaurants-inspection-oksmivk4fqfcwxeprrwjvp32ii.us-east-1.es.amazonaws.com/_search', auth=aws_auth)
print(json.loads(req.text))
"""

print('Loading function')
dynamo = boto3.client('dynamodb')


def getRestaurants(longitude, latitude, cuisine, hygieneGrade, priceGrade, restaurantName, distance):
    """get nearby restaurants based on location and other criterias"""
    # TODO Elastic search, now we use dummy data

    return [{ "restaurantId": "415",
            "cuisine": "Taiwanese",
            "address": "5th ave",
            "phone": "9298887777",
            "name": "Papa john's",
            "longitude": 154.1234,
            "latitude": 14.1234,
            "hygieneGrade": "A",
            "priceGrade": "$"}, { "restaurantId": "123",
            "cuisine": "Indian",
            "address": "5th ave",
            "phone": "9298887777",
            "name": "Mama john's",
            "longitude": 154.1234,
            "latitude": 14.1234,
            "hygieneGrade": "A",
            "priceGrade": "$$"}]

def getRestaurantInfo(restaurantId):
    """get full information for a restaurant"""
    # TODO DynamoDB, , now we use dummy data
    return {
          "address": "string",
          "phone": "9298887777",
          "name": "Papa john's",
          "longitude": 154.1234,
          "latitude": 14.1234,
          "hygieneGrade": "A",
          "priceGrade": "$",
          "comments": [
            "string"
          ]
        }

def respond(err, res=None):
    return {
        'statusCode': '400' if err else '200',
        'body': str(err) if err else json.dumps(res),
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
    }


def lambda_handler(event, context):
    '''Demonstrates a simple HTTP endpoint using API Gateway. You have full
    access to the request and response payload, including headers and
    status code.

    To scan a DynamoDB table, make a GET request with the TableName as a
    query string parameter. To put, update, or delete an item, make a POST,
    PUT, or DELETE request respectively, passing in the payload to the
    DynamoDB API as a JSON body.
    '''
    """
    operations = {
        'DELETE': lambda dynamo, x: dynamo.delete_item(**x),
        'GET': lambda dynamo, x: dynamo.scan(**x),
        'POST': lambda dynamo, x: dynamo.put_item(**x),
        'PUT': lambda dynamo, x: dynamo.update_item(**x),
    }
    """
    operation = event['httpMethod']
    if operation == 'GET':
        if event['resource'] == '/{restaurantId}':
            result = getRestaurantInfo(event["pathParameters"]["restaurantId"])

        elif event['resource'] == '/restaurants':
            # check if userLocation is present
            longitude = event['queryStringParameters'].get('longitude')
            latitude = event['queryStringParameters'].get('latitude')
            if not longitude or not latitude:
                return respond(ValueError('userLocation not found'))

            cuisine = event['queryStringParameters'].get('cuisine')
            hygieneGrade = event['queryStringParameters'].get('hygieneGrade')
            priceGrade = event['queryStringParameters'].get('priceGrade')
            restaurantName = event['queryStringParameters'].get('restaurantName')
            distance = event['queryStringParameters'].get('distance')
            if not distance:
                distance = 100
            result = getRestaurants(longitude, latitude, cuisine, hygieneGrade, priceGrade, restaurantName, distance)

        else:
            # only support previous two resources
            return respond(ValueError('Unsupported resource "{}"'.format(event['resource'])))
        return respond(None, result)
    else:
        return respond(ValueError('Unsupported method "{}"'.format(operation)))
