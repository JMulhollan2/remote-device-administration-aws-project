import json
import requests
import os
import webbrowser

# Imports all information modules
from get_location import get_location
from get_time import get_time
from get_user import get_user
from get_platform import get_platform

device_credentials_bool = False

# For now, hardcoded API endpoints. Replace with pipeline/lambda params if time permits.
ngrok_url = ""
api_url = "https://bws1po3z0l.execute-api.eu-west-1.amazonaws.com/dev"

print ("Welcome to Telemetry, your device is not yet configured.")
print ("Please follow the instructions below to get started.")

# Loop that runs checks against information entered
while (device_credentials_bool != True):
    email_correct_bool = False

    # Validation on the email for a valid address, length check also
    while (email_correct_bool != True):
        email_input = input("Please type your Telemetry account email: ")
        if "@" in email_input:
            if len(str(email_input)) > 64:
                print("Sorry, this email is too long.")
            else:
                email_correct_bool = True
        else:
            print("Sorry, this email was not recognised.")    

    # Gets device key - validation done next
    api_key_input = input("Please paste your device key found in the web console: ")

    # Gets name of device and checks against DB to ensure it isn't duplicated
    device_name_input = input("Enter a name for the device: ")
    r = requests.get(api_url+"/get-device-data", headers = {'Email': email_input,'APIKey': api_key_input,'DeviceName': device_name_input})
    if ("Device does not exist" in r.text):
        r2 = requests.post(api_url+"/add-device", headers = {'Email': email_input,'APIKey': api_key_input,'DeviceName': device_name_input, 'DeviceLastOnline': get_time(), 'CurrentUser': get_user(), 'Platform': get_platform(),"DeviceLocation": str(get_location())})
        if (r2.status_code == 200):
            device_credentials_bool = True
        else:
            print (r2.text)
            print ("Please try again.")
    elif (r.status_code == 200):
        print("Sorry, this device name already exists on your account, try another name!")
    else:
        print (r.text)
        print ("Please try again.")

# Creates the JSON file, opens the website
json_data = {
    "user-email": email_input, 
    "ngrok-address": ngrok_url, 
    "device-name": device_name_input, 
    "user-api-key": api_key_input, 
    "desktop-api": api_url
    }
with open('config.json', 'w') as outfile:  
    json.dump(json_data, outfile)
print  ("Device added!")
webbrowser.open('https://www.telemetry-tracking.com/devicewelcome.html')

# Once run, launches the launch manager again
os.startfile('launch-manager.exe')