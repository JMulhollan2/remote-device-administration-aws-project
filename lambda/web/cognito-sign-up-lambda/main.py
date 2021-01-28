import boto3
import random
import string

dynamodb = boto3.client('dynamodb')

# Adds a user to the DynamoDB table with information supplied from Cognito as a "PreSignUpLambda"
def add_user(TableName, email):
    item_check = dynamodb.get_item(TableName=TableName,Key={'Email':{'S':email}})
    try:
        item_check['Item']
        print ('User already exists, returning true but not manipulating table.')
        return True
    except:
        print('User does not exist, allowing table manipluation...')
        APIKey = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(30))
        HasProfilePicture = False
        table_item = {'Email': {'S': email}, 'AccountType': {'S': 'user'}, 'APIKey': {'S': APIKey}, 'HasProfilePicture': {'BOOL': HasProfilePicture}}
        dynamodb.put_item(TableName=TableName,Item=table_item)
        return True

# Main handler
def handler(event, context):
    email = event['userName']
    # Hardcoded table name - shoulld be lambda param in future supplied by CodePipeline
    TableName = "ProjectDynamoDBTable"

    if add_user(TableName, email):
        return event
    else:
        return


    #event['response']['autoConfirmUser'] = True # Lil debug option to speed up account testing

    