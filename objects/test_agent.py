import time
import os

from frequency_analyzer import FrequencyAnalyzer
from sound_modifier import SoundModifier
from audio_recognizer import AudioRecognizer
from text_compare import TextComparer
from api_bridge import ApiBridge
from variables import *
from device_io import DeviceIO 
from audio_recognizer import AudioRecognizer
from constants import *


class TestAgent:

    def __init__(self, uri):
        self.bridge = ApiBridge('wss://cpclientapi.softphone.com:9002/counterpath/socketapi/v1')
        self.io = DeviceIO()
        self.io.loadFile(os.getcwd() + "./test-data/weekday1.wav")
        

    def io_setup(self):
    
        self.bridge.open_connection();
        
        self.io.setDevices()
        self.devices = self.bridge.get_device_info()
        
        dId = self.devices[WIN_IN_B]
        self.bridge.set_device(WIN_IN_B, dId, 'output', 'headset')

        dId = self.devices[WIN_OUT_A]
        self.bridge.set_device(WIN_OUT_A, dId, 'input', 'headset')
        
        self.bridge.close_connection()
     

    def two_point_zero_one(self):
        
        self.bridge.open_connection();
        print(self.bridge.place_call(REMOTEEND))

        time.sleep(5)
        self.io.loadFile(os.getcwd() + "./test-data/weekday1.wav")
        self.io.playRecord(os.getcwd() + "./outputs/test1.wav")

        output = AudioRecognizer.work(os.getcwd() + "./outputs/test1.wav")

        TextComparer.compareOutputToFile("./test-data/word_list.txt", output)
        self.bridge.close_connection()