import boto3
import json

dynamodb = boto3.client('dynamodb')

# Parses DB table to return device data for specific user
def get_device_data(DeviceName, db_item):
    for device in db_item['AssignedDevices']['L']:
        if device['M']['DeviceName']['S'] == DeviceName:
            return {'statusCode': 200,'body': json.dumps(device['M'])}
        else:
            pass
    return {'statusCode': 500,'body': json.dumps('Error: Internal error has occured.. something to do with the device_data loop... :(')}

# Checks to ensure a device does exist in the table
def check_device_name(db_item, DeviceName):
    # Check if any devices already exist
    try:
        AssignedDevices = db_item['AssignedDevices']
    except:
        AssignedDevices = False

    # Not an ideal way to check, however it saves parsing device data which is a lot of work and shouldn't cause any issues
    if str("'DeviceName': {'S': '"+DeviceName+"'}") not in str(AssignedDevices):
        return True
    else:
        return False

# Main handler
def handler(event, context):
    # Hardcoded, should be added as a Lambda param in the future with a deployment pipeline
    TableName = "ProjectDynamoDBTable"
    # Get headers from API event
    try:
        Email = (json.dumps(event['headers']['Email'])).strip('"')
        APIKey = (json.dumps(event['headers']['APIKey'])).strip('"')
        DeviceName = (json.dumps(event['headers']['DeviceName'])).strip('"')
    except:
        return {'statusCode': 500,'body': json.dumps('Error: Not all headers were entered')}

    # Get user data from db
    try:
        db_response = dynamodb.get_item(TableName=TableName, Key={'Email':{'S':Email}})
        db_item = db_response['Item']
        db_APIKey = list((db_item['APIKey']).values())[0]
    except:
        return {'statusCode': 500,'body': json.dumps('Error: Unable to return database entry. Likely user does not exist.')}

    # Match up device API key to authorise
    if (db_APIKey == APIKey):
        print ('Provided API key matches database key, authorised.')
    else:
        print ('Error: API Key does not match key on record')
        return {'statusCode': 500,'body': json.dumps('Error: API Key does not match key on record')}

    # Validation for device name, then return  device data
    if check_device_name(db_item, DeviceName):
        return {'statusCode': 500,'body': json.dumps('Error: Device does not exist')}
    else:
        return get_device_data(DeviceName, db_item)
        

    