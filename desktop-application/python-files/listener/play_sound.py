import json
import winsound
import time

def play_sound():
    winsound.PlaySound('sound.wav', winsound.SND_FILENAME)
    time.sleep(.5)
    winsound.PlaySound('sound.wav', winsound.SND_FILENAME)
    time.sleep(.5)
    winsound.PlaySound('sound.wav', winsound.SND_FILENAME)