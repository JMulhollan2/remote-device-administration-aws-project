import boto3
import json

dynamodb = boto3.client('dynamodb')

# Todo - in the event I want the ability to modify user data
def get_user_data():
    print("Todo - in the event that I add more user data I want to be able to manipulate.")

# Main handler, simply returns user data to populate web console
def handler(event, context):
    TableName = "ProjectDynamoDBTable"
    email = event['requestContext']['authorizer']['claims']['email']

    response = dynamodb.get_item(TableName=TableName, Key={'Email':{'S': email}})
    user_data = response['Item']

    print(user_data)

    return {'statusCode': 200,'body': json.dumps(user_data), "headers": { "Access-Control-Allow-Origin": "*" }}