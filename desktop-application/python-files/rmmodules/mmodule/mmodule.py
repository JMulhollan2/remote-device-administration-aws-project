import win32com.client
import os
import time
import subprocess
import sys

# Module simply manages rmodule, the main module. Opens it if it's closed.
def manage_rmodule():
    # Monitors Windows processes
    strComputer = "."
    objWMIService = win32com.client.Dispatch("WbemScripting.SWbemLocator")
    objSWbemServices = objWMIService.ConnectServer(strComputer,"root\cimv2")
    colItems = objSWbemServices.ExecQuery("Select * from Win32_Process")

    rmodule_alive = False

    for objItem in colItems:
        if (objItem.Name == "rmodule.exe"):
            rmodule_alive = True

    if rmodule_alive == False:
        print ("ALERT: Rmodule is offline")
        CREATE_NO_WINDOW = 0x08000000
        subprocess.Popen('rmodule.exe', creationflags=CREATE_NO_WINDOW)
        quit()

# Checks every second to see if rmodule is running
while 1:
    manage_rmodule()
    time.sleep(1)