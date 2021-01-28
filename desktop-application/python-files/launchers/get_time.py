import json
import time

def get_time():
    timestamp = time.time()
    timestamp = (str(timestamp).replace(".", ""))[:-4]
    return timestamp