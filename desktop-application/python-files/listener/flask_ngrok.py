#################
# Adapted by James Mulholland from https://github.com/gstaff/flask-ngrok
#################

import atexit
import json
import os
import platform
import shutil
import subprocess
import tempfile
import time
import zipfile
from pathlib import Path
from threading import Timer
import requests


def _run_ngrok():
    ngrok_path = str(Path(tempfile.gettempdir(), "ngrok"))
    _download_ngrok(ngrok_path)
    system = platform.system()
    if system == "Darwin":
        command = "ngrok"
    elif system == "Windows":
        command = "ngrok.exe"
    elif system == "Linux":
        command = "ngrok"
    else:
        raise Exception("{system} is not supported")
    executable = str(Path(ngrok_path, command))
    os.chmod(executable, 777)

    CREATE_NO_WINDOW = 0x08000000
    ngrok = subprocess.Popen([executable, 'http', '5000'], creationflags=CREATE_NO_WINDOW)
    atexit.register(ngrok.terminate)
    localhost_url = "http://localhost:4040/api/tunnels"  # Url with tunnel details
    time.sleep(1)
    tunnel_url = requests.get(localhost_url).text  # Get the tunnel information
    j = json.loads(tunnel_url)

    tunnel_url = j['tunnels'][0]['public_url']  # Do the parsing of the get request to find the public URL of the device
    tunnel_url = tunnel_url.replace("https", "http")
    return tunnel_url


def _download_ngrok(ngrok_path):
    if Path(ngrok_path).exists():
        return
    system = platform.system()
    if system == "Darwin":
        url = "https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-darwin-amd64.zip"
    elif system == "Windows":
        url = "https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-windows-amd64.zip"
    elif system == "Linux":
        url = "https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-linux-amd64.zip"
    else:
        raise Exception("{system} is not supported")
    download_path = _download_file(url)
    with zipfile.ZipFile(download_path, "r") as zip_ref:
        zip_ref.extractall(ngrok_path)


def _download_file(url):
    local_filename = url.split('/')[-1]
    r = requests.get(url, stream=True)
    download_path = str(Path(tempfile.gettempdir(), local_filename))
    with open(download_path, 'wb') as f:
        shutil.copyfileobj(r.raw, f)
    return download_path


def start_ngrok():
    ngrok_address = _run_ngrok()
    update_config_with_address(ngrok_address) # Update config with ngrok address of the device
    print(" * Running on " + ngrok_address)


def run_with_ngrok(app):
    """
    The provided Flask app will be securely exposed to the public internet via ngrok when run,
    and the its ngrok address will be printed to stdout
    """
    old_run = app.run

    def new_run():
        thread = Timer(1, start_ngrok)
        thread.setDaemon(True)
        thread.start()
        old_run()
    app.run = new_run

# Function to update config with NGROK address, added by James
def update_config_with_address(ngrok_address):
    with open('config.json', 'r+') as f:
        data = json.load(f)
        data['ngrok-address'] = ngrok_address
        f.seek(0)
        json.dump(data, f, indent=4)
        f.truncate() 