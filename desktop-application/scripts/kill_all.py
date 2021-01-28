import os
import time

os.system("TASKKILL /F /IM mmodule.exe")
os.system("TASKKILL /F /IM rmodule.exe")
os.system("TASKKILL /F /IM telservice.exe")
os.system("TASKKILL /F /IM ngrok.exe")

time.sleep(10)