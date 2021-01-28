import requests
import boto3
import time

print ("Running tests!")

dynamodb = boto3.client('dynamodb')
TableName = "ProjectDynamoDBTable"

# Info for the throwaway user
APIKey = "TestAPIKey"
Email = "testscript@automatedtest.com"

# Adds test user
test_user = {'Email': {'S': Email}, 'AccountType': {'S': 'user'}, 'APIKey': {'S': APIKey}}
dynamodb.put_item(TableName=TableName,Item=test_user)

# API Tests

# File info
f= open("testresult.txt","w+")
f.write("Telemetry test report \n")
f.write(" \n")
f.write("Generated user: "+Email+" \n")
f.write("API key used: "+APIKey+" \n")
f.write(" \n")
f.write("DESKTOP API TESTS: \n")
f.write(" \n")

#####################################
# Desktop add device API
#####################################
f.write("ADD DEVICE - POST \n")
api_url = "https://bws1po3z0l.execute-api.eu-west-1.amazonaws.com/dev/add-device"

# Legal request
r = requests.post(api_url, headers = {'Email': Email,'APIKey': APIKey,'DeviceName': "TestDevice1", 'DeviceLastOnline': 'Test', 'DeviceLocation': 'Test', 'Platform': 'Test', 'CurrentUser': 'Test'})
if (r.status_code == 200):
    result = "Pass"
else:
    result = ("Fail: "+str(r.status_code)+", "+r.text)
f.write("Legal request: "+str(result)+" \n")

# Illegal request with not all params
r = requests.post(api_url, headers = {'Email': Email,'APIKey': APIKey,'DeviceName': "TestDevice2", 'DeviceLastOnline': 'Test', 'DeviceLocation': 'Test', 'Platform': 'Test'})
if "Not all paramaters were entered" in r.text:
    result = "Pass"
else:
    result = ("Fail: "+str(r.status_code)+", "+r.text)
f.write("Illegal request (Not all parameters): "+str(result)+" \n")

# Illegal request duplicate device
r = requests.post(api_url, headers = {'Email': Email,'APIKey': APIKey,'DeviceName': "TestDevice1", 'DeviceLastOnline': 'Test', 'DeviceLocation': 'Test', 'Platform': 'Test', 'CurrentUser': 'Test'})
if "Device name already in use" in r.text:
    result = "Pass"
else:
    result = ("Fail: "+str(r.status_code)+", "+r.text)
f.write("Illegal request (Duplicate device): "+str(result)+" \n")

# Illegal request wrong API key
r = requests.post(api_url, headers = {'Email': Email,'APIKey': "WrongKey",'DeviceName': "TestDevice2", 'DeviceLastOnline': 'Test', 'DeviceLocation': 'Test', 'Platform': 'Test', 'CurrentUser': 'Test'})
if "API Key does not match key on record" in r.text:
    result = "Pass"
else:
    result = ("Fail: "+str(r.status_code)+", "+r.text)
f.write("Illegal request (Incorrect API Key): "+str(result)+" \n")

# Illegal request max devices
r = requests.post(api_url, headers = {'Email': Email,'APIKey': APIKey,'DeviceName': "TestDevice2", 'DeviceLastOnline': 'Test', 'DeviceLocation': 'Test', 'Platform': 'Test', 'CurrentUser': 'Test'})
time.sleep(1)
r = requests.post(api_url, headers = {'Email': Email,'APIKey': APIKey,'DeviceName': "TestDevice3", 'DeviceLastOnline': 'Test', 'DeviceLocation': 'Test', 'Platform': 'Test', 'CurrentUser': 'Test'})
time.sleep(1)
r = requests.post(api_url, headers = {'Email': Email,'APIKey': APIKey,'DeviceName': "TestDevice4", 'DeviceLastOnline': 'Test', 'DeviceLocation': 'Test', 'Platform': 'Test', 'CurrentUser': 'Test'})
time.sleep(1)

r = requests.post(api_url, headers = {'Email': Email,'APIKey': APIKey,'DeviceName': "TestDevice5", 'DeviceLastOnline': 'Test', 'DeviceLocation': 'Test', 'Platform': 'Test', 'CurrentUser': 'Test'})
if "Max number of devices reached on this account" in r.text:
    result = "Pass"
else:
    result = ("Fail: "+str(r.status_code)+", "+r.text)
f.write("Illegal request (Max number of devices): "+str(result)+" \n")

f.write(" \n")

#####################################
# Desktop GET Api
#####################################
f.write("GET DEVICE DATA - GET \n")
api_url = "https://bws1po3z0l.execute-api.eu-west-1.amazonaws.com/dev/get-device-data"

# Legal Request
r = requests.get(api_url, headers = {'Email': Email,'APIKey': APIKey,'DeviceName': "TestDevice1"})
if (r.status_code == 200):
    result = "Pass"
else:
    result = ("Fail: "+str(r.status_code)+", "+r.text)
f.write("Legal request: "+str(result)+" \n")

# Illegal Request not all headers
r = requests.get(api_url, headers = {'Email': Email,'APIKey': APIKey})
if "Not all headers were entered" in r.text:
    result = "Pass"
else:
    result = ("Fail: "+str(r.status_code)+", "+r.text)
f.write("Illegal request (Not all headers): "+str(result)+" \n")

# Illegal Request not all headers
r = requests.get(api_url, headers = {'Email': Email,'APIKey': APIKey,'DeviceName': "TestDevice0"})
if "Device does not exist" in r.text:
    result = "Pass"
else:
    result = ("Fail: "+str(r.status_code)+", "+r.text)
f.write("Illegal request (Device not exist): "+str(result)+" \n")

# Illegal Request wrong API key
r = requests.get(api_url, headers = {'Email': Email,'APIKey': "WrongKey",'DeviceName': "TestDevice1"})
if "API Key does not match key on record" in r.text:
    result = "Pass"
else:
    result = ("Fail: "+str(r.status_code)+", "+r.text)
f.write("Illegal request (Wrong API key): "+str(result)+" \n")

# Illegal Request wrong email
r = requests.get(api_url, headers = {'Email': "wrong@wrong.com",'APIKey': "WrongKey",'DeviceName': "TestDevice1"})
if "Likely user does not exist" in r.text:
    result = "Pass"
else:
    result = ("Fail: "+str(r.status_code)+", "+r.text)
f.write("Illegal request (Wrong email): "+str(result)+" \n")

f.write(" \n")

#####################################
# Desktop modify device POST API
#####################################
f.write("MODIFY DEVICE DATA - POST \n")
api_url = "https://bws1po3z0l.execute-api.eu-west-1.amazonaws.com/dev/update-db"

# Legal Request
r = requests.post(api_url, headers = {'Email': Email,'APIKey': APIKey, 'DeviceName': "TestDevice1", "DataType": "Device", "AttributeToUpdate": "Platform", "UpdateValue": "Test"})
if (r.status_code == 200):
    result = "Pass"
else:
    result = ("Fail: "+str(r.status_code)+", "+r.text)
f.write("Legal request: "+str(result)+" \n")

# Illegal Request wrong email
r = requests.post(api_url, headers = {'Email': "wrong@wrong.com",'APIKey': APIKey, 'DeviceName': "TestDevice1", "DataType": "Device", "AttributeToUpdate": "Platform", "UpdateValue": "Test"})
if "Likely user does not exist" in r.text:
    result = "Pass"
else:
    result = ("Fail: "+str(r.status_code)+", "+r.text)
f.write("Illegal request (Wrong email): "+str(result)+" \n")

# Illegal Request not all headers
r = requests.post(api_url, headers = {'Email': Email, 'APIKey': APIKey, 'DeviceName': "TestDevice1", "DataType": "Device", "AttributeToUpdate": "Platform"})
if "Not all paramaters were entered" in r.text:
    result = "Pass"
else:
    result = ("Fail: "+str(r.status_code)+", "+r.text)
f.write("Illegal request (Not all parameters): "+str(result)+" \n")

# Illegal Request wrong API key
r = requests.post(api_url, headers = {'Email': Email,'APIKey': "WrongAPIKey", 'DeviceName': "TestDevice1", "DataType": "Device", "AttributeToUpdate": "Platform", "UpdateValue": "Test"})
if "API Key for this user does not match stored API key" in r.text:
    result = "Pass"
else:
    result = ("Fail: "+str(r.status_code)+", "+r.text)
f.write("Illegal request (Wrong API key): "+str(result)+" \n")

# Closes file
f.close()

# Deletes user
dynamodb.delete_item(TableName=TableName,Key={"Email": {"S": Email}})