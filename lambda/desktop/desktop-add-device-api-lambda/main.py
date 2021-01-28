import boto3
import json
import ast

dynamodb = boto3.client('dynamodb')

max_devices_allowed = 4

# Method invoked when user tries to add a new device to their user
def add_device(db_item, TableName, Email, DeviceName, DeviceLastOnline, DeviceLocation, DevicePlatform, CurrentUser):
    # Check if devices already exist in the DynamoDB table
    try:
        AssignedDevices = db_item['AssignedDevices']
        Device1 = AssignedDevices['L'][0]
        ExistingDevices = True   
    except:
        ExistingDevices = False
    
    # Adds a new entry to the user's devices updating the JSON list of devices
    if ExistingDevices:
        new_device_db_json = ",{'M': {'RequestedFileDownload': {'BOOL': False}, 'DeviceLastOnline': {'S': '"+DeviceLastOnline+"'}, 'HasRequestedFileDownload': {'BOOL': False}, 'HasRequestedFileEncryption': {'BOOL': False}, 'RemoteLockEnabled': {'BOOL': False}, 'RemoteLocationEnabled': {'BOOL': False}, 'DeviceLocation': {'S': '"+DeviceLocation+"'}, 'RequestedFileEncryption': {'BOOL': False}, 'DeviceStatus': {'S': 'Online'}, 'NgrokUrl': {'S': 'null'}, 'HasRequestedFileSystem': {'BOOL': False}, 'RemoteWipeEnabled': {'BOOL': False}, 'RemoteLogoutEnabled': {'BOOL': False}, 'Platform': {'S': '"+DevicePlatform+"'}, 'CurrentUser': {'S': '"+CurrentUser+"'}, 'RemoteLockPasscode': {'S': 'null'}, 'RemoteSoundEnabled': {'BOOL': False}, 'DeviceName': {'S': '"+DeviceName+"'}}}]}"
        assigned_devices_to_join = str(AssignedDevices)[:-2]
        joined_devices_db_json = ast.literal_eval(assigned_devices_to_join+new_device_db_json)
        try:
            dynamodb.update_item(TableName=TableName, Key={'Email':{'S':Email}}, UpdateExpression="set AssignedDevices = :r",ExpressionAttributeValues={':r': joined_devices_db_json})
            return {'statusCode': 200,'body': json.dumps('Success')}
        except:
            print("Error updating table")
            return {'statusCode': 500,'body': json.dumps('Error: Unable to update DynamoDB table')}   
    else:
        new_device_db_json = "{'L': [{'M': {'RequestedFileDownload': {'BOOL': False}, 'DeviceLastOnline': {'S': '"+DeviceLastOnline+"'}, 'HasRequestedFileDownload': {'BOOL': False}, 'HasRequestedFileEncryption': {'BOOL': False}, 'RemoteLockEnabled': {'BOOL': False}, 'RemoteLocationEnabled': {'BOOL': False}, 'DeviceLocation': {'S': '"+DeviceLocation+"'}, 'RequestedFileEncryption': {'BOOL': False}, 'DeviceStatus': {'S': 'Online'}, 'NgrokUrl': {'S': 'null'}, 'HasRequestedFileSystem': {'BOOL': False}, 'RemoteWipeEnabled': {'BOOL': False}, 'RemoteLogoutEnabled': {'BOOL': False}, 'Platform': {'S': '"+DevicePlatform+"'}, 'CurrentUser': {'S': '"+CurrentUser+"'}, 'RemoteLockPasscode': {'S': 'null'}, 'RemoteSoundEnabled': {'BOOL': False}, 'DeviceName': {'S': '"+DeviceName+"'}}}]}"
        try:
            dynamodb.update_item(TableName=TableName, Key={'Email':{'S':Email}}, UpdateExpression="set AssignedDevices = :r",ExpressionAttributeValues={':r': ast.literal_eval(new_device_db_json)})
            return {'statusCode': 200,'body': json.dumps('Success')}
        except:
            print("Error updating table")
            return {'statusCode': 500,'body': json.dumps('Error: Unable to update DynamoDB table')}

# Runs a check to ensure a user does not already have the max no. of devices on their account (4)
def check_max_no_devices(db_item):
    # Enforces a limit on how many devices can be added per account
    try:
        AssignedDevices = db_item['AssignedDevices']
    except:
        AssignedDevices = False

    if (AssignedDevices == False):
        return True
    else:
        devices_count = len(AssignedDevices['L'])
        if devices_count < max_devices_allowed:
            return True
        else:
            return False

# Checks to see if a device already exists for a user
def check_device_name(db_item, DeviceName):
    # Check if any devices already exist
    try:
        AssignedDevices = db_item['AssignedDevices']
    except:
        AssignedDevices = False

    # Not an ideal way to check, however it saves parsing device data which is a lot of work and shouldn't cause any issues. With more time could be perfected.
    if str("'DeviceName': {'S': '"+DeviceName+"'}") not in str(AssignedDevices):
        return True
    else:
        return False

# Man Lambda handler
def handler(event, context):
    # Hardcoded, ideally passed as a paremeter in a deployment pipleine
    TableName = "ProjectDynamoDBTable"

    # Get headers from event
    try:
        Email = (json.dumps(event['headers']['Email'])).strip('"')
        APIKey = (json.dumps(event['headers']['APIKey'])).strip('"')
        DeviceName = (json.dumps(event['headers']['DeviceName'])).strip('"')
        DeviceLastOnline = (json.dumps(event['headers']['DeviceLastOnline'])).strip('"')
        DeviceLocation = (json.dumps(event['headers']['DeviceLocation'])).strip('"')
        DevicePlatform = (json.dumps(event['headers']['Platform'])).strip('"')
        CurrentUser = (json.dumps(event['headers']['CurrentUser'])).strip('"')
    except:
        return {'statusCode': 400,'body': json.dumps('Error: Not all paramaters were entered.')}

    # Get user data from db
    try:
        db_response = dynamodb.get_item(TableName=TableName, Key={'Email':{'S':Email}})
        db_item = db_response['Item']
        db_APIKey = list((db_item['APIKey']).values())[0]
    except:
        return {'statusCode': 500,'body': json.dumps('Error: Unable to return database entry. Likely user does not exist.')}
    
    # Match up API key to authorise
    if (db_APIKey == APIKey):
        print ('Provided API key matches database key, authorised.')
    else:
        print ('Error: API Key does not match key on record')
        return {'statusCode': 500,'body': json.dumps('Error: API Key does not match key on record')}

    # Validation for device name - ensure it is not being duplicated
    if check_device_name(db_item, DeviceName):
        if check_max_no_devices(db_item):
            return add_device(db_item, TableName, Email, DeviceName, DeviceLastOnline, DeviceLocation, DevicePlatform, CurrentUser)
        else:
            return {'statusCode': 500,'body': json.dumps('Error: Max number of devices reached on this account')}
    else:
        return {'statusCode': 500,'body': json.dumps('Error: Device name already in use')}