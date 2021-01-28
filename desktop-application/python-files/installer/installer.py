import os
import time
import sys
import ctypes
from distutils.dir_util import copy_tree
from shutil import copy
from shutil import copytree
import subprocess
import webbrowser

def install_telemetry():
    # Copy files to Telservice directory
    print("Installing telemetry files...")
    try:
        copytree("telemetry-files", "C:/Telservice")
    except Exception as err:
        print (err)

    # Add telservice startup executable & python dll file to startup directory
    print ("Setting up startup service...")
    try:
        copy("startup/telstartup.exe", "C:/ProgramData/Microsoft/Windows/Start Menu/Programs/StartUp")
        copy("startup/python37.dll", "C:/ProgramData/Microsoft/Windows/Start Menu/Programs/StartUp")
    except Exception as err:
        print (err)

    # Launch telservice for first time, open launch manager
    print ("Launching Telemetry...")
    os.chdir('C:/Telservice')
    os.startfile('launch-manager.exe')
    print ("Telemetry installed and running.")

# Checks if open as admin
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

# Ensures program is open as admin
if is_admin():
    install_telemetry()
else:
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)