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

def do(action):
        ActionClicker.doAction(action)

class TestAgent:

    def __init__(self, uri=None):
        
        self.bridge = ApiBridge(WEBSOCKET_ADDRESS)
        self.io = DeviceIO()
        self.io.setDevices()
        self.briaArea = None
        
        
    def test_audio(self):
        self.io.loadFile(os.getcwd() + "./test-data/weekday1.wav")
        self.io.playRecord(os.getcwd() + "./outputs/test1.wav")

        output = AudioRecognizer.work(os.getcwd() + "./outputs/test1.wav")

        TextComparer.compareOutputToFile("./test-data/weekday1.txt", output)

    def test_incoming_call(self):
        time.sleep(5)
        ActionClicker.switchToRemote(NUM_ENDS,0)
        ActionClicker.dial(END_A);
        do("Call")
    
        ActionClicker.backToLocal()
        time.sleep(3)
        do("Answer")
		
        time.sleep(5)
        self.io.loadFile(os.getcwd() + "./test-data/weekday1.wav")
        self.io.playRecord(os.getcwd() + "./outputs/test1.wav")

        output = AudioRecognizer.work(os.getcwd() + "./outputs/test1.wav")

        TextComparer.compareOutputToFile("./test-data/weekday1.txt", output)

        do("EndCall")

    def test_outgoing_call(self):
        time.sleep(5)

        ActionClicker.dial(END_B);
        do("Call")
    
        time.sleep(2)

        ActionClicker.switchToRemote(NUM_ENDS,0)

        do("Answer")
		
        ActionClicker.backToLocal()
        
        time.sleep(2)
        self.io.loadFile(os.getcwd() + "./test-data/weekday1.wav")
        self.io.playRecord(os.getcwd() + "./outputs/test2.wav")

        output = AudioRecognizer.work(os.getcwd() + "./outputs/test2.wav")

        TextComparer.compareOutputToFile("./test-data/weekday1.txt", output)

        do("EndCall")


    def test_mute(self):
        time.sleep(5)
        
        ActionClicker.dial(END_B);
        do("Call")
    
        time.sleep(2)

        ActionClicker.switchToRemote(NUM_ENDS,0)

        do("Answer")
		
        ActionClicker.backToLocal()
        
        do("Mute")

        time.sleep(2)
        self.io.loadFile(os.getcwd() + "./test-data/weekday1.wav")
        self.io.playRecord(os.getcwd() + "./outputs/mute1.wav")

        output = AudioRecognizer.work(os.getcwd() + "./outputs/mute1.wav")
        print(TextComparer.isBlank(output))

        do("Mute")

        self.io.loadFile(os.getcwd() + "./test-data/weekday1.wav")
        self.io.playRecord(os.getcwd() + "./outputs/mute1.wav")

        output = AudioRecognizer.work(os.getcwd() + "./outputs/mute1.wav")
        TextComparer.compareOutputToFile("./test-data/weekday1.txt", output)

        do("EndCall")

    def test_hold(self):
        time.sleep(5)
        
        ActionClicker.dial(END_B)
        do("Call")
    
        time.sleep(2)

        ActionClicker.switchToRemote(NUM_ENDS,0)

        do("Answer")
		
        ActionClicker.backToLocal()
        time.sleep(2)

        do("Hold")

        time.sleep(2)
        self.io.loadFile(os.getcwd() + "./test-data/weekday1.wav")
        self.io.playRecord(os.getcwd() + "./outputs/mute1.wav")

        output = AudioRecognizer.work(os.getcwd() + "./outputs/mute1.wav")
        print(TextComparer.isBlank(output))

        time.sleep(2)

        do("Unhold")

        self.io.loadFile(os.getcwd() + "./test-data/weekday1.wav")
        self.io.playRecord(os.getcwd() + "./outputs/mute1.wav")

        output = AudioRecognizer.work(os.getcwd() + "./outputs/mute1.wav")
        TextComparer.compareOutputToFile("./test-data/weekday1.txt", output)

        do("EndCall")
		
    def speaker_mode(self):
        do("Speaker")
        self.test_outgoing_call()
        do("Headset")
        
    def video_start(self):
        
        do("Contacts")
        do("ContSearch")
        ActionClicker.type(END_B_NAME)
        do("VideoCall1")
        
        ActionClicker.switchToRemote(NUM_ENDS, 0)
        
        time.sleep(3)
        
        do("VideoAccept")
        
        ActionClicker.backToLocal()
        
        time.sleep(10)
        
        do("Center")
        
        time.sleep(1)
        
        offset = ScreenScanner.verifyVideo()
        
        do("EndVideo")
        time.sleep(5)
        do("ClearContactSearch")
        
    def video_upgrade(self):
        time.sleep(5)
        ActionClicker.switchToRemote(NUM_ENDS,0)
        ActionClicker.dial(END_A);
        do("Call")
    
        ActionClicker.backToLocal()
        time.sleep(3)
        do("Answer")
        time.sleep(2)
        do("UpgradeVideo")
        ActionClicker.switchToRemote(NUM_ENDS,0)
        do("UpgradeVideo")
        
        ActionClicker.backToLocal()
        time.sleep(8)
        
        offset = ScreenScanner.verifyVideo()
        
        do("EndVideo")
        
    def receive_transfer(self, transferType):
        time.sleep(5)

        ActionClicker.switchToRemote(NUM_ENDS,1)

        ActionClicker.dial(END_B)
        do("Call")

        time.sleep(2)
        
        ActionClicker.backToLocal()
        ActionClicker.switchToRemote(NUM_ENDS,0)
        do("Answer")
        
        time.sleep(2)
        
        ActionClicker.transfer(END_A, transferType)
        
        ActionClicker.backToLocal()
        
        time.sleep(3)
        
        do("Answer")
        
        self.testAudio()
        
        do("EndCall")
        
    def call_swap(self):
        time.sleep(5)

        ActionClicker.switchToRemote(NUM_ENDS,1)

        ActionClicker.dial(END_A)
        do("Call")

        time.sleep(2)
        
        ActionClicker.backToLocal()
        ActionClicker.switchToRemote(NUM_ENDS,0)
        ActionClicker.dial(END_A)
        do("Call")
        ActionClicker.backToLocal()
        
        time.sleep(2)
        do("Answer")
        time.sleep(2)
        
        do("Swap2")
        
        self.test_audio(self)
        
        do("Swap1")
        
        self.test_audio(self)
        
        do("EndCall")
        
        time.sleep(2)
        
        do("EndCall")
        
    def MWI(self):
        time.sleep(5)

        ActionClicker.dial(END_B);
        do("Call")
    
        time.sleep(2)

        ActionClicker.switchToRemote(NUM_ENDS,0)

        do("Answer")
		
        ActionClicker.backToLocal()
        
        time.sleep(2)
        
        screen_scanner.checkForImage("MWI.png", self.briaArea)
        
        do("EndCall")

    
    def contactCall(self):
        do("Contacts")
        do("ContSearch")
        ActionClicker.type(END_B_NAME)
        do("ContactCall1")
        
        ActionClicker.switchToRemote(NUM_ENDS, 0)
        
        time.sleep(3)
        
        do("Answer")
        
        ActionClicker.backToLocal()
        
        self.testAudio()

        do("EndCall")
        
        do("ClearContactSearch")     
   
   
    def historyCall(self):
        time.sleep(5)
        
        do("History")
        do("HistoryCall1")
        
        ActionClicker.switchToRemote(NUM_ENDS, 0)
        
        time.sleep(3)
        
        do("Answer")
        
        ActionClicker.backToLocal()
                
        time.sleep(1)
        
        self.testAudio()
        
        do("EndCall")
        
   
    def verifyPresence(self):
        time.sleep(5)

        ActionClicker.dial(END_B);
        do("Call")
    
        time.sleep(2)

        ActionClicker.switchToRemote(NUM_ENDS,0)

        do("Answer")
		
        ActionClicker.backToLocal()
        
        ActionClicker.endCall()