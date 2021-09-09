import sys
import numpy as np
import matplotlib.pyplot as plt
from scipy.io.wavfile import read, write
import scipy.signal as sps
from IPython.display import Audio
from numpy.fft import fft, ifft

sys.path.append('s./env/Lib/site-packages')
import librosa

sys.path.append('.')
from frequency_analyzer import FrequencyAnalyzer
from sound_modifier import SoundModifier
from audio_recognizer import AudioRecognizer
from text_compare import TextComparer
from api_bridge import ApiBridge
from variables import *
from device_io import DeviceIO 

io = DeviceIO()
bridge = ApiBridge('wss://cpclientapi.softphone.com:9002/counterpath/socketapi/v1')

io.setDevices()
io.loadFile("weekday1.wav")

print(bridge.open_connection())
print(bridge.send_message(api_request_types['CALL'], '<?xml version="1.0" encoding="utf-8" ?><dial type="audio"><number>7035</number><displayName>Bro</displayName><suppressMainWindow>false</suppressMainWindow>'))

bridge.wait(10)

print(bridge._get_all_responses())
#io.playRecord("test1.wav")

print(bridge.close_connection())

#output = AudioRecognizer.work("test1.wav")

#TextComparer.compareOutputToFile("word_list.txt", output)


