import os
import boto3
import json
import ast

dynamodb = boto3.client('dynamodb')

# This method will process device data to be modified, and modify the DynamoDB table (e.g. change device name)
def process_user_data(TableName, Email, APIKey, DataType, DeviceName, AttributeToUpdate, UpdateValue):
    # Required for testing API Key before anything else
    try:
        db_response = dynamodb.get_item(TableName=TableName, Key={'Email':{'S':Email}})
        db_item = db_response['Item']
        db_APIKey = list((db_item['APIKey']).values())[0]
    except:
        return {'statusCode': 500,'body': json.dumps('Error: Unable to return database entry. Likely user does not exist.')}

    # Tests API key, then downloads device data, modifies it, and overwrites table data.
    if (db_APIKey == APIKey):
        print ('Provided API key matches database key, authorised.')

        # Supports only changes to Device data currently, supplied by a header called "AttributeToUpdate"
        if DataType == "User": # Decides if device data needs to be got - currently always yes due to no requirements otherwise.
            print ("A user data type was entered. This build does not support this.")
            return {'statusCode': 500,'body': json.dumps('Error: A user data type was entered. This build does not support this.')}

        # Some less than ideal string matching/modification to update the DynamoDB table, mainly due to the NoSQL architecture
        elif DataType == "Device":
            db_devices = (db_item['AssignedDevices'])
            parsed_db_devices = db_devices['L'] # (List) Parses all the weird DynamoDB lists with different dicts in it
            for device in parsed_db_devices:
                if (list((device['M']['DeviceName']).values())[0]) == DeviceName: # Finds the correct device in the for loop
                    device_attribute = device['M'][AttributeToUpdate] # Device attribute - used in string replace
                    dynamodb_json_device_attribute = "'"+str(AttributeToUpdate)+"': "+str(device_attribute) # Creates what a full entry in DynamoDB would look like for a replacement, to avoid replacing multiple entries in a table if they are the same value
                    parsed_device_attribute = list((device['M'][AttributeToUpdate]).values())[0] # Removes DynamoDb JSON - so the value can be replaced
                    new_device_attribute = "'"+str(AttributeToUpdate)+"': "+(str(device_attribute).replace(str(parsed_device_attribute), str(UpdateValue))) # New value, with DynamoDB JSON added
                    new_device_data = str(device['M']).replace(str(dynamodb_json_device_attribute), str(new_device_attribute)) # New set of device attributes, needs to be added to device list
                    updated_db_devices = ast.literal_eval(str(db_devices).replace(str(device['M']), new_device_data)) # New device list, ready to be added to DynamoDB, replacing the old list
                    return update_devices_in_db(TableName, Email, updated_db_devices)
                else:
                    pass

        elif DataType == "OfflineCommand":
            print ("An offline command data type was entered. This build does not support this.")
            return {'statusCode': 500,'body': json.dumps('Error: A offline command data type was entered. This build does not support this.')}
    else:
        return {'statusCode': 401,'body': json.dumps('Error: API Key for this user does not match stored API key')}

# Unfinished - would have allowed for user name changes etc
def update_user_attribute(TableName, Email, dynamodb_data_type, AttributeToUpdate, UpdateValue):
    try:
        dynamodb.put_item(TableName=TableName, Item={AttributeToUpdate:{dynamodb_data_type: UpdateValue}})
        return {'statusCode': 200,'body': json.dumps('Success')}
    except:
        return {'statusCode': 500,'body': json.dumps('Error: Unable to update table.')}        

# Takes the updated JSON statement of a user's devices and replaces the current staatement in DynamoDB
def update_devices_in_db(TableName, Email, updated_db_devices):
    try:
        dynamodb.update_item(
            TableName=TableName, 
            Key={'Email':{'S':Email}}, 
            UpdateExpression="set AssignedDevices = :i", # This will require a param if anything but device data is changed
            ExpressionAttributeValues={':i': updated_db_devices}
        )
        return {'statusCode': 200,'body': json.dumps('Success')}
    except:
        return {'statusCode': 500,'body': json.dumps('Error: Unable to update table.')}

# Main handler
def handler(event, context):
    #DEVICES_TABLE = boto3.resource('dynamodb').Table(os.environ['DEVICES_TABLE']) # Requires env variable set
    # Hardcoded - ideally should be a Lambda param in the future and set from deployment pipeline
    TableName = "ProjectDynamoDBTable"

    # Pull headers from API request
    try:
        Email = (json.dumps(event['headers']['Email'])).strip('"')
        APIKey = (json.dumps(event['headers']['APIKey'])).strip('"')
        DataType = (json.dumps(event['headers']['DataType'])).strip('"')
        AttributeToUpdate = (json.dumps(event['headers']['AttributeToUpdate'])).strip('"')
        UpdateValue = (json.dumps(event['headers']['UpdateValue'])).strip('"')
    except:
        return {'statusCode': 400,'body': json.dumps('Error: Not all paramaters were entered.')}

    # Picks up all table changes on DynamoDB table, so this ensures the change is device-specific
    if DataType != 'Device':
        DeviceName = False
    else:
        try:
            DeviceName = (json.dumps(event['headers']['DeviceName'])).strip('"')
        except:
            return {'statusCode': 400,'body': json.dumps('Error: Not all paramaters were entered.')}


    print("Printing event")
    print (json.dumps(event))
    print("Event printed")

    return process_user_data(TableName, Email, APIKey, DataType, DeviceName, AttributeToUpdate, UpdateValue)
