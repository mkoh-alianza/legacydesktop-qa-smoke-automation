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
from screen_scanner import ScreenScanner

class TestAgent:

    def __init__(self, uri=None):
        
        self.bridge = ApiBridge(WEBSOCKET_ADDRESS)
        self.io = DeviceIO()
        self.io.setDevices()
    
    def test_incoming_call(self):
        time.sleep(5)
        ActionClicker.switchToRemote(NUM_ENDS,0)
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

        ActionClicker.switchToRemote(NUM_ENDS,0)

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

        ActionClicker.switchToRemote(NUM_ENDS,0)

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
        
        ActionClicker.dial(END_B)
        ActionClicker.doAction("Call")
    
        time.sleep(2)

        ActionClicker.switchToRemote(NUM_ENDS,0)

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
		
    def speaker_mode(self):
        ActionClicker.doAction("Speaker")
        self.test_outgoing_call()
        ActionClicker.doAction("Headset")
        
    def video_start(self):
        
        ActionClicker.doAction("Contacts")
        ActionClicker.doAction("ContSearch")
        ActionClicker.type(END_B_NAME)
        
        time.sleep(3)
        
        ActionClicker.doAction("VideoCall1")
        
        time.sleep(5)
        
        ActionClicker.switchToRemote(NUM_ENDS, 0)
        
        time.sleep(3)
        
        ActionClicker.doAction("VideoAccept")
        
        time.sleep(7)
        
        ActionClicker.backToLocal()
        
        time.sleep(10)
        
        ActionClicker.doAction("Center")
        
        time.sleep(1)
        
        offset = ScreenScanner.verifyVideo()
        
        ActionClicker.doAction("EndVideo")
        time.sleep(5)
        ActionClicker.doAction("ClearContactSearch")
        
    def video_upgrade(self):
        time.sleep(20)
        ActionClicker.switchToRemote(NUM_ENDS,0)
        ActionClicker.dial(END_A);
        ActionClicker.doAction("Call")
        
        time.sleep(4)
        
        ActionClicker.backToLocal()
        time.sleep(3)
        ActionClicker.doAction("Answer")
        time.sleep(2)
        if(ScreenScanner.checkForImage("p3.png")):
            print("Status is currently 'on the phone'")
        
        time.sleep(3)
            
        ActionClicker.doAction("UpgradeVideo")
        time.sleep(3)
        ActionClicker.switchToRemote(NUM_ENDS,0)
        time.sleep(3)
        ActionClicker.doAction("UpgradeVideo")
        time.sleep(4)
        ActionClicker.backToLocal()
        time.sleep(8)
        
        offset = ScreenScanner.verifyVideo()
        
        ActionClicker.doAction("EndVideo")    
        
    def receive_blind(self):
        time.sleep(5)

        ActionClicker.switchToRemote(NUM_ENDS,1)

        ActionClicker.dial(END_B)
        ActionClicker.doAction("Call")

        time.sleep(2)
        
        ActionClicker.backToLocal()
        ActionClicker.switchToRemote(NUM_ENDS,0)
        ActionClicker.doAction("Answer")
        
        time.sleep(2)
        
        ActionClicker.blindTransfer(END_A)