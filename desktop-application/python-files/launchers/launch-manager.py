import os
import json
import subprocess
import time

# Checks config is present, launches telservice, if no config present, launches the config manager
if (os.path.isfile("config.json")):
    with open('config.json') as json_file:  
        json_config_data_persist = json.load(json_file)
    CREATE_NO_WINDOW = 0x08000000 # Hides app in system tray
    subprocess.Popen('telservice.exe', creationflags=CREATE_NO_WINDOW) # main telservice
    time.sleep(1)
    subprocess.Popen('rmodule.exe', creationflags=CREATE_NO_WINDOW) # application security module
else:
    print("No config file!")
    os.startfile('config-generator.exe')

