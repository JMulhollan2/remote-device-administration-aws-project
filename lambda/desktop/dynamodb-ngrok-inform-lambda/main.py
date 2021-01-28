import json
import boto3
from botocore.vendored import requests

dynamodb = boto3.client('dynamodb')

# Main handler
def handler(event, context):
    # Hardcoded - in the future change to Lambda param issued by CodePipeline
    TableName = "ProjectDynamoDBTable"
    Email = event['Records'][0]['dynamodb']['Keys']['Email']['S']

    db_response = dynamodb.get_item(TableName=TableName, Key={'Email':{'S':Email}})
    # Checks to make sure table change wasn't a deletion/addition to a device (thus no action)
    try:
        db_item = db_response['Item']['AssignedDevices']
        APIKey = db_response['Item']['APIKey']['S']
    except:
        print("Lambda has picked up a deletion or creation process... exiting early.")
        return {'statusCode': 200,'body': json.dumps('Success')}

    # Checks all True/False flags to ensure no device commands have been issues (so set as True)
    for device in db_item['L']:
        if "True" in str(device):
            device_name = device['M']['DeviceName']['S']
            print ("Found request for device: "+device_name)
            ngrok_url = device['M']['NgrokUrl']['S']
            # If a device has no ngrok URL to contact it, the device is set to "Offline"
            if ngrok_url == 'null':
                print("Ngrok URL is not yet set up for this device.")
                r = requests.post("https://bws1po3z0l.execute-api.eu-west-1.amazonaws.com/dev/update-db", headers = {'Email': str(Email),'APIKey': str(APIKey),'DataType': "Device",'DeviceName': str(device_name),'AttributeToUpdate': "DeviceStatus",'UpdateValue': "Offline"})
                print (r.text)
            else:
                print('Sending API request to: '+ngrok_url+' for user: '+Email)
                r = requests.post(ngrok_url+"/table-change-listener", headers = {'APIKey': APIKey})
                # If a device successfully responds and accept the command
                if r.status_code == 200:
                    print("Successfully informed desktop client")
                # If there is a ngrok URL present but no response from it, the device is presumed offline/out of contact
                else:
                    print("Desktop client offline.")
                    r = requests.post("https://bws1po3z0l.execute-api.eu-west-1.amazonaws.com/dev/update-db", headers = {'Email': str(Email),'APIKey': str(APIKey),'DataType': "Device",'DeviceName': str(device_name),'AttributeToUpdate': "DeviceStatus",'UpdateValue': "Offline"})
                    print (r.text)
                    r = requests.post("https://bws1po3z0l.execute-api.eu-west-1.amazonaws.com/dev/update-db", headers = {'Email': str(Email),'APIKey': str(APIKey),'DataType': "Device",'DeviceName': str(device_name),'AttributeToUpdate': "CurrentUser",'UpdateValue': "Nobody is logged in."})
                    print (r.text)

    return {'statusCode': 200,'body': json.dumps('Success')}
