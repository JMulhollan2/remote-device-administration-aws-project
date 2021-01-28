import json
import time

def get_time():
    raw_timestamp = time.time()
    int_timestamp = (str(raw_timestamp).replace(".", ""))

    string_cut_value = len(str(int_timestamp)) - 13

    if (string_cut_value == -2):
        timestamp = str(int_timestamp)+"00"
    elif (string_cut_value == -1):
        timestamp = str(int_timestamp)+"0"
    elif (string_cut_value == 0):
        timestamp = str(int_timestamp)
    else:
        timestamp = str(int_timestamp)[:((string_cut_value)*-1)]

    return timestamp