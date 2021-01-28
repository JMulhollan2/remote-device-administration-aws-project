import boto3
import json
from botocore.vendored import requests

dynamodb = boto3.client('dynamodb')
# Hardcoded, good in future to change to Lambda parameter supplied via CodePipeline
TableName = "ProjectDynamoDBTable"

# Deletes a device by parsing list of devices, removing device, recompliling list of devices, updating table
def delete_device(DeviceName, Email):
    db_response = dynamodb.get_item(TableName=TableName, Key={'Email':{'S':Email}})
    db_item = db_response['Item']
    db_devices = (db_item['AssignedDevices'])
    parsed_db_devices = db_devices['L'] # (List) Parses all the weird DynamoDB lists with different dicts in it

    # Sets up a new array for which to add the new device list minus the deleted device
    new_parsed_db_devices = []

    # Adds devices to new device list, minus deleted device
    for device in parsed_db_devices:
        if (list((device['M']['DeviceName']).values())[0]) == DeviceName:
            print("Found device to delete, not adding to updates list...")
        else:
            new_parsed_db_devices.append(device)
        
    # Adds DynamoDB formatting, then sends update request to DynamoDB
    new_db_devices = {"L": new_parsed_db_devices}
    try:
        dynamodb.update_item(
            TableName=TableName, 
            Key={'Email':{'S':Email}}, 
            UpdateExpression="set AssignedDevices = :i",
            ExpressionAttributeValues={':i': new_db_devices}
        )
        return {'statusCode': 200,'body': json.dumps('Success')}
    except:
        return {'statusCode': 500,'body': json.dumps('Error: Unable to update table.')}

# Main handler
def handler(event, context):
    TableName = "ProjectDynamoDBTable"
    # Hardcoded table param, should be lambda param in future supplied by CodePipeline
    user_email = event['requestContext']['authorizer']['claims']['email']

    response = dynamodb.get_item(TableName=TableName, Key={'Email':{'S': user_email}})
    APIKey = response['Item']['APIKey']['S']

    print(json.dumps(event['headers']))

    # Logic to work out what type of request based off API headers- ideally this would get split into a seperate lambda but this saves time and a lot of re-doing of authentication steps
    try:
        DeviceName = (json.dumps(event['headers']['devicename'])).strip('"')
        DataType = (json.dumps(event['headers']['datatype'])).strip('"')
        AttributeToUpdate = (json.dumps(event['headers']['attributetoupdate'])).strip('"')
        UpdateValue = (json.dumps(event['headers']['updatevalue'])).strip('"')
        DeviceModificationHeaders = True
    except:
        print ("Device modification headers do not exist.")
        DeviceModificationHeaders = False
    
    try:
        DeviceName = (json.dumps(event['headers']['devicename'])).strip('"')
        DeleteDeviceBool = (json.dumps(event['headers']['deletedevicebool'])).strip('"')
        DeviceDeleteHeaders = True
    except:
        print ("Device delete headers do not exist.")
        DeviceDeleteHeaders = False

    # Executes different logic depending on what type of request
    if DeviceModificationHeaders:
        # Proxies request to the desktop API, this saves time whilst retaining security
        print ("Modification of field "+ AttributeToUpdate +" for "+ DeviceName + " on account "+ user_email + " in progress")
        r = requests.post("https://bws1po3z0l.execute-api.eu-west-1.amazonaws.com/dev/update-db", headers = {'Email': user_email,'APIKey': APIKey,'DataType': DataType,'DeviceName': DeviceName,'AttributeToUpdate': AttributeToUpdate,'UpdateValue': UpdateValue})
        if r.status_code == 200:
            return {'statusCode': 200,'body': json.dumps("Success"), "headers": { "Access-Control-Allow-Origin": "*" }}
        else:
            return {'statusCode': 500,'body': json.dumps("Error updating table!"), "headers": { "Access-Control-Allow-Origin": "*" }}
    elif DeviceDeleteHeaders:
        print ("Device deletion for "+ DeviceName + " on account "+ user_email + " in progress")
        delete_device(DeviceName, user_email)
        return {'statusCode': 200,'body': json.dumps("Success"), "headers": { "Access-Control-Allow-Origin": "*" }}
    else:
        print("Headers were not provided correctly.")
        return {'statusCode': 500,'body': json.dumps("Error, required headers do not exist."), "headers": { "Access-Control-Allow-Origin": "*" }}