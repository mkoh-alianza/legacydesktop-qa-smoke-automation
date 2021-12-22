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
from action_clicker import ActionClicker

class TestAgent:

    def __init__(self, uri):
        
        self.bridge = ApiBridge('wss://cpclientapi.softphone.com:9002/counterpath/socketapi/v1')
        self.io = DeviceIO()
        self.io.setDevices()

    def io_setup(self):
    
        self.io.setDevices()

    
    def test_incoming_call(self):
        time.sleep(5)
        ActionClicker.switchToRemote(1,0)
        ActionClicker.dial(END_A);
        ActionClicker.doAction("Call")
    
        ActionClicker.backToLocal()
        time.sleep(3)
        ActionClicker.doAction("Answer")
		
        time.sleep(5)
        self.io.loadFile(os.getcwd() + "./test-data/weekday1.wav")
        self.io.playRecord(os.getcwd() + "./outputs/test1.wav")

        output = AudioRecognizer.work(os.getcwd() + "./outputs/test1.wav")

        TextComparer.compareOutputToFile("./test-data/weekday1.txt", output)

        ActionClicker.doAction("EndCall")

    def test_outgoing_call(self):
        time.sleep(5)

        ActionClicker.dial(END_B);
        ActionClicker.doAction("Call")
    
        time.sleep(2)

        ActionClicker.switchToRemote(1,0)

        ActionClicker.doAction("Answer")
		
        ActionClicker.backToLocal()
        
        time.sleep(2)
        self.io.loadFile(os.getcwd() + "./test-data/weekday1.wav")
        self.io.playRecord(os.getcwd() + "./outputs/test2.wav")

        output = AudioRecognizer.work(os.getcwd() + "./outputs/test2.wav")

        TextComparer.compareOutputToFile("./test-data/weekday1.txt", output)

        ActionClicker.doAction("EndCall")


    def test_mute(self):
        time.sleep(5)
        
        ActionClicker.dial(END_B);
        ActionClicker.doAction("Call")
    
        time.sleep(2)

        ActionClicker.switchToRemote(1,0)

        ActionClicker.doAction("Answer")
		
        ActionClicker.backToLocal()
        
        ActionClicker.doAction("Mute")

        time.sleep(2)
        self.io.loadFile(os.getcwd() + "./test-data/weekday1.wav")
        self.io.playRecord(os.getcwd() + "./outputs/mute1.wav")

        output = AudioRecognizer.work(os.getcwd() + "./outputs/mute1.wav")
        print(TextComparer.isBlank(output))

        ActionClicker.doAction("Mute")

        self.io.loadFile(os.getcwd() + "./test-data/weekday1.wav")
        self.io.playRecord(os.getcwd() + "./outputs/mute1.wav")

        output = AudioRecognizer.work(os.getcwd() + "./outputs/mute1.wav")
        TextComparer.compareOutputToFile("./test-data/weekday1.txt", output)

        ActionClicker.doAction("EndCall")

    def test_hold(self):
        time.sleep(5)
        
        ActionClicker.dial(END_B);
        ActionClicker.doAction("Call")
    
        time.sleep(2)

        ActionClicker.switchToRemote(1,0)

        ActionClicker.doAction("Answer")
		
        ActionClicker.backToLocal()
        time.sleep(2)

        ActionClicker.doAction("Hold")

        time.sleep(2)
        self.io.loadFile(os.getcwd() + "./test-data/weekday1.wav")
        self.io.playRecord(os.getcwd() + "./outputs/mute1.wav")

        output = AudioRecognizer.work(os.getcwd() + "./outputs/mute1.wav")
        print(TextComparer.isBlank(output))

        time.sleep(2)

        ActionClicker.doAction("Unhold")

        self.io.loadFile(os.getcwd() + "./test-data/weekday1.wav")
        self.io.playRecord(os.getcwd() + "./outputs/mute1.wav")

        output = AudioRecognizer.work(os.getcwd() + "./outputs/mute1.wav")
        TextComparer.compareOutputToFile("./test-data/weekday1.txt", output)

        ActionClicker.doAction("EndCall")
		
    def receive_transfer(self):
        time.sleep(5)