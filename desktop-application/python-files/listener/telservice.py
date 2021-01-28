from flask import Flask, jsonify, request
from flask_ngrok import run_with_ngrok
import json
import os
import time
import requests
import threading

# Imports all the functions for different tasks/information
from get_location import get_location
from play_sound import play_sound
from get_time import get_time
from get_user import get_user
from get_platform import get_platform
from wipe_device import wipe_device
from log_out_device import log_out_device

app = Flask(__name__)
run_with_ngrok(app)  # Start ngrok when app is run

# Health check section to establish connection with server and check in with it + send device status, also run at app start. 
@app.route('/health-check', methods=['GET'])
def health_check():
    print('Recieved health check request')

    try: 
        APIKeyHeader = request.headers.get('APIKey')
    except:
        print ("API Key not provided.")
        return "No API key provided!"

    # Open config file and load config ready to communicate with AWS environment
    with open('config.json') as json_file:  
        data = json.load(json_file)
        api_url = data['desktop-api']
        ngrok_url = data['ngrok-address']
        user_email = data['user-email']
        api_key = data['user-api-key']
        device_name = data['device-name']

    # Exchanges information with DB, could be made efficient with one API call in the future
    if APIKeyHeader == api_key:
        print(ngrok_url)
        r = requests.post(api_url+"/update-db", headers = {'Email': user_email,'APIKey': api_key,'DataType': 'Device','DeviceName': device_name,'AttributeToUpdate': 'NgrokUrl','UpdateValue': ngrok_url})
        if r.status_code == 200:
            print("Successfully informed db of ngrok url")
            requests.post(api_url+"/update-db", headers = {'Email': user_email,'APIKey': api_key,'DataType': 'Device','DeviceName': device_name,'AttributeToUpdate': 'DeviceStatus','UpdateValue': "Online"})
            current_time = get_time()
            requests.post(api_url+"/update-db", headers = {'Email': user_email,'APIKey': api_key,'DataType': 'Device','DeviceName': device_name,'AttributeToUpdate': 'DeviceLastOnline','UpdateValue': current_time})
            current_platform = get_platform()
            requests.post(api_url+"/update-db", headers = {'Email': user_email,'APIKey': api_key,'DataType': 'Device','DeviceName': device_name,'AttributeToUpdate': 'Platform','UpdateValue': current_platform})
            current_user = get_user()
            requests.post(api_url+"/update-db", headers = {'Email': user_email,'APIKey': api_key,'DataType': 'Device','DeviceName': device_name,'AttributeToUpdate': 'CurrentUser','UpdateValue': current_user})
        else:
            print(r)
        # Runs check of table to check no actions are outstanding
        check_table()
        return "API alive!"
    else:
        return ("API Key does not match item stored on record.")

# Checks table and performs any actions the database lists as outstanding (e.g. Remote shutdown command is pending)
@app.route('/table-change-listener', methods=['POST'])
def check_table():
    try:
        APIKeyHeader = request.headers.get('APIKey')
        print ("API Key provided: "+APIKeyHeader)
    except:
        print ("API Key not provided.")
        return "No API key provided!"

    print('Checking table for changes...')
    # Open config file and load config ready to communicate with AWS environment
    with open('config.json') as json_file:  
        data = json.load(json_file)
        api_url = data['desktop-api']
        user_email = data['user-email']
        api_key = data['user-api-key']
        device_name = data['device-name']

    # If statement ensures API key matches key on record to ensure request is authenticated
    if APIKeyHeader == api_key:
        # Gets relevant device data to check if outstanding commands present
        r = requests.get(api_url+"/get-device-data", headers = {'Email': user_email,'APIKey': api_key,'DeviceName': device_name})
        if r.status_code == 200:
            device_data = json.loads(r.content)
            remote_wipe_enabled = device_data['RemoteWipeEnabled']['BOOL']
            remote_sound_enabled = device_data['RemoteSoundEnabled']['BOOL']
            remote_location_enabled = device_data['RemoteLocationEnabled']['BOOL']
            remote_logout_enabled = device_data['RemoteLogoutEnabled']['BOOL']
        elif ("Device does not exist" in r.text):
            device_not_exist()
        else:
            print("Error getting table data")
        
        # In the event the app was offline, the device will update the db to show that the device is online
        requests.post(api_url+"/update-db", headers = {'Email': user_email,'APIKey': api_key,'DataType': 'Device','DeviceName': device_name,'AttributeToUpdate': 'DeviceStatus','UpdateValue': "Online"})

        # Logic for issuing device commands based off information queued in db
        if remote_location_enabled:
            device_location = get_location()
            print ("Location requested!")
            inform_table("DeviceLocation", str(device_location))
            inform_table("RemoteLocationEnabled", "False")
        if remote_wipe_enabled:
            print (" Remote wipe enabled.")
            wipe_device()
            log_out_device()
        if remote_sound_enabled:
            play_sound()
            inform_table("RemoteSoundEnabled", "False")
        if remote_logout_enabled:
            inform_table("RemoteLogoutEnabled", "False")
            log_out_device()

        # Updates information of device on DB, again could be formed into one API request for efficiency 
        current_time = get_time()
        requests.post(api_url+"/update-db", headers = {'Email': user_email,'APIKey': api_key,'DataType': 'Device','DeviceName': device_name,'AttributeToUpdate': 'DeviceLastOnline','UpdateValue': current_time})
        current_platform = get_platform()
        requests.post(api_url+"/update-db", headers = {'Email': user_email,'APIKey': api_key,'DataType': 'Device','DeviceName': device_name,'AttributeToUpdate': 'Platform','UpdateValue': current_platform})
        current_user = get_user()
        requests.post(api_url+"/update-db", headers = {'Email': user_email,'APIKey': api_key,'DataType': 'Device','DeviceName': device_name,'AttributeToUpdate': 'CurrentUser','UpdateValue': current_user})
        return jsonify(' Request recieved by desktop app ')
    else:
        return ("API Key does not match item stored on record.")

# In the event the device is deleted, this will delete the config and force the program to open the config menu at next restart
def device_not_exist():
    try:
        os.remove("C:/ProgramData/Telbackup/Program/config.json")
    except:
        print ("Config file backup already removed")
    
    try:
        os.remove("C:/Telservice/config.json")
    except:
        print ("Config file already removed")

# Update main db with device information
def inform_table(update_attribute, update_value):
    with open('config.json') as json_file:  
        data = json.load(json_file)
        api_url = data['desktop-api']
        user_email = data['user-email']
        api_key = data['user-api-key']
        device_name = data['device-name']

    r = requests.post(api_url+"/update-db", headers = {'Email': user_email,'APIKey': api_key,'DataType': 'Device','DeviceName': device_name,'AttributeToUpdate': update_attribute,'UpdateValue': update_value})
    print(r)

# Main function start
def start_runner():
    def start_loop():
        with open('config.json') as json_file:  
            data = json.load(json_file)
            api_key = data['user-api-key']
        
        # Small loop/delay to wait for ngrok service to start up and to wait for request/response to itself
        count = 0
        time.sleep(10)
        while count <= 10:
            print('In start loop')
            try:
                r = requests.get('http://127.0.0.1:5000/health-check', headers = {'APIKey': api_key})
                if r.status_code == 200:
                    print('Server started, quiting start_loop')
                    count = 10
                print(r.status_code)
            except:
                print('Server not yet started')
            time.sleep(2)
            count = count+1
            
    # Hourly check as a heartbeat back to the server
    def hourly_health_check():
        time.sleep(60)
        try:
            with open('config.json') as json_file:  
                data = json.load(json_file)
                api_key = data['user-api-key']
        except:
            print("Config file does not exist")

        while True:
            time.sleep(3600)
            requests.get('http://127.0.0.1:5000/health-check', headers = {'APIKey': api_key})

    print('Started runner')
    thread1 = threading.Thread(target=start_loop)
    thread2 = threading.Thread(target=hourly_health_check)
    thread1.start()
    thread2.start()

if __name__ == '__main__':
    start_runner()
    app.run()
