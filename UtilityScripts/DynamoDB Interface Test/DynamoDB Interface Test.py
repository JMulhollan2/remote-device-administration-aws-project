import boto3

client = boto3.client('dynamodb')

response = client.get_item(TableName='TestUsersTable', Key={'UserID':{'S':'A1'}})

print(response)