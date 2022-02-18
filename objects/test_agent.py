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
from uem_bridge import UemBridge
#login'er 

def do(action):
        ActionClicker.doAction(action)

class TestAgent:

    def __init__(self, uri=None):
        
        self.bridge = ApiBridge(WEBSOCKET_ADDRESS)
        self.io = DeviceIO()
        self.io.setDevices()
        self.briaArea = None
        self.uem = UemBridge(UEM_ADDRESS, SRETTO_USERNAME, SRETTO_PASSWORD)
        
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

        ActionClicker.dial(END_B)
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
      #TODO must add logic for attended transfers
    def receive_transfer(self, transferType):
        time.sleep(5)

        ActionClicker.switchToRemote(NUM_ENDS,1)

        ActionClicker.dial(END_B)
        do("Call")

        time.sleep(2)
        
        ActionClicker.backToLocal()
        ActionClicker.switchToRemote(NUM_ENDS,0)
        do("Answer")
        
        time.sleep(4)
        
        ActionClicker.backToLocal()
        ActionClicker.switchToRemote(NUM_ENDS,1)
        
        time.sleep(4)
        
        ActionClicker.transfer(END_A, transferType)
        
        ActionClicker.backToLocal()
        
        time.sleep(3)
        
        do("AnswerRegular")
        
        self.test_audio()
        
        do("EndCall")
        
    def call_swap(self):
        time.sleep(5)

        ActionClicker.switchToRemote(NUM_ENDS,1)

        ActionClicker.dial(END_A)
        do("Call")

        time.sleep(2)
        
        ActionClicker.backToLocal()
        
        time.sleep(2)
        do("Answer")
        
        ActionClicker.switchToRemote(NUM_ENDS,0)
        ActionClicker.dial(END_A)
        do("Call")
        ActionClicker.backToLocal()
        
        time.sleep(2)
        do("Answer2")
        time.sleep(2)
        
        self.test_audio()
        
        do("Swap1")
        
        #self.test_audio()
        
        do("Swap2")
        
        self.test_audio()
        
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
        
        screen_scanner.checkForImage("MWI", self.briaArea)
        
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
        
        do("HistoryTab")
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

        ScreenScanner.checkForImage("p2")

        ActionClicker.dial(END_B);
        do("Call")
    
        time.sleep(2)

        ActionClicker.switchToRemote(NUM_ENDS,0)

        do("Answer")
		
        ActionClicker.backToLocal()

        ScreenScanner.checkForImage("p3")
        
        ActionClicker.endCall()
        
    def createContact(self, testNo):
        time.sleep(5)
        
        do("Contacts")
        do("AddContact")
        do("ContactDisplay")
        ActionClicker.type("Display Test" + TestNo)
        do("ContactFirstName")
        ActionClicker.type(TestNo+" First")
        do("ContactLastName")
        ActionClicker.type(TestNo+" Last")
        do("ContactSoftphone")
        ActionClicker.type("1112")
        do("ContactAddNum")
        do("SaveContact")
        
        do("ContSearch")
        ActionClicker.type(TestNo)
        
        ScreenScnaner.checkForImage("ContactExists")
        
        do("ClearContactSearch")
        
    def verifyMissedCall(self):
        time.sleep(5)
        
        do("Dialpad")
        
        ActionClicker.switchToRemote(NUM_ENDS, 0)
        
        ActionClicker.dial(END_B);
        do("Call")
        
        ActionClicker.backToLocal();
        
        time.sleep(20)
        
        ScreenScanner.checkForImage("1MissedCall")
        
        
    def contactPresence(self):
        time.sleep(5)
        
        ActionClicker.switchToRemote(NUM_ENDS, 0)
        
        do("SetPresenceBusy")
        
        ActionClicker.backToLocal()
        
        do("Contacts")
        do("ContSearch")
        ActionClicker.type(END_B_NAME)
        
        ScreenScanner.checkForImage("ContactBusyPresence")
        
        ActionClicker.switchToRemote(NUM_ENDS, 0)
        
        do("SetPresenceAvailable")
        
        ActionClicker.backToLocal()
        
    def receiveIM(self):
        time.sleep(5)
        
        ActionClicker.switchToRemote(NUM_ENDS, 0)
        
        do("GoToMessageSearch")
        
        ActionClicker.type(END_A_NAME)
        
        do("MessageTopIMResult")
        
        ActionClicker.type("test", time=0.1)
        ActionClicker.pressKey('enter')
        ActionClicker.type("test", time=0.1)
        ActionClicker.pressKey('enter')
        ActionClicker.type("test", time=0.1)
        ActionClicker.pressKey('enter')
        
        ActionClicker.backToLocal()
        time.sleep(1)
        
        print(ScreenScanner.checkForImage("IMAlert"))
        
        time.sleep(1)
        
        print(ScreenScanner.checkForImage("IMAlert"))
        
    def call_recording(self):
        time.sleep(5)

        ActionClicker.dial(END_B);
        do("Call")
    
        time.sleep(2)

        ActionClicker.switchToRemote(NUM_ENDS,0)

        do("Answer")
		
        ActionClicker.backToLocal()
        
        do("toggleTopCallRecording")
        
        time.sleep(2)
        self.io.loadFile(os.getcwd() + "./test-data/weekday1.wav")
        self.io.play(os.getcwd() + "./test-data/weekday1.wav")

        do("toggleTopCallRecording")
		
        time.sleep(3)
        
        do("EndCall")

        time.sleep(2)

        output = AudioRecognizer.work(RECORDING_PATH + '/' + AudioRecognizer.findNewestRecording(RECORDING_PATH))

        TextComparer.compareOutputToFile("./test-data/weekday1.txt", output)

    def send_log(self, testNo):
        do("ToSendLogReportTxt")
        ActionClicker.type("This is a test log send by an automated script. Is test number " + testNo)

        do("SendReport")

        ScreenScanner.checkForImage("LogSent")
		
    def check_user_portal(self):
        do("UserPortalTab")

        ScreenScanner.checkForImage("LogSent")


    def check_uem_vqm(self):
        self.uem.open_connection()
        self.test_incoming_call()
        name = self.uem.query("vqm", "imap.mobilevoiplive.com", "MOS_BIN_CQ")

        print(self.uem.getNumReports(name))
        
        
    def check_uem_analytics(self):
        self.uem.open_connection()
        self.test_incoming_call()
        name = self.uem.query("analytics", "imap.mobilevoiplive.com", "CALLS_INCOMING")

        print(self.uem.getNumReports(name))
    
    
    def private_chatroom(self):
        do("GoToCreateChat")
        
        do("ChatRoomPrivate")
        
        do("SetChatRoomName")
        
        ActionClicker.type("Private")
        
        do("CreateChatRoom")
        
        time.sleep(2)
        
        ScreenScanner.checkForImage("PrivateChat")
        
        do("DeleteTopRoom")
        
    def public_chatroom(self):
        do("GoToCreateChat")

        do("ChatRoomPublic")
        
        do("SetChatRoomName")
        
        ActionClicker.type("Public")
        
        do("CreateChatRoom")
        
        time.sleep(2)
        
        ScreenScanner.checkForImage("PublicChat")
        
        do("DeleteTopRoom")
    
    def host_screen_share(self):
        
        do("Contacts")
        do("ContSearch")
        ActionClicker.type(END_B_NAME)
        
        do("StartScreenShare")
        
        ActionClicker.switchToRemote(NUM_ENDS, 0)
        
        area = ScreenScanner.findImage("JoinScreenshare")
        
        ActionClicker.clickAt(area[0], area[1])
        
        time.sleep(2)
        
        print(ScreenScanner.checkForImage("SmallScreenShareImage"))
        
        do("CloseScreenShare")
        
        ActionClicker.backToLocal()
        
        do("EndScreenShare")
        
        do("ClearContactSearch")