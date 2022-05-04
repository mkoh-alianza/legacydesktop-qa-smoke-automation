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
def wait(tim):
    time.sleep(tim + 4)
    
class TestAgent:

    def __init__(self, uri=None):
        
        self.bridge = ApiBridge(WEBSOCKET_ADDRESS)
        self.io = DeviceIO()
        self.io.setDevices()
        self.briaArea = ScreenScanner.findBria()
        self.uem = UemBridge(UEM_ADDRESS, SRETTO_USERNAME, SRETTO_PASSWORD)

    def do(self, action):
        return ActionClicker.doAction(action)
    def wait(self, tim):
        time.sleep(self, tim + 4)
    def find(self, img):
        return ScreenScanner.findImage(img)
    
    def clickAt(self, coords):
        ActionClicker.clickAt(coords)
    
    def test_audio(self, file = None):
        self.io.loadFile(os.getcwd() + "./test-data/weekday1.wav")
        self.io.playRecord(os.getcwd() + "./outputs/test1.wav")

        output = AudioRecognizer.work(os.getcwd() + "./outputs/test1.wav")

        TextComparer.compareOutputToFile("./test-data/weekday1.txt", output)

    def test_incoming_call(self):
        wait(5)
        
        ActionClicker.switchToRemote(NUM_ENDS,0)
        ActionClicker.dial(END_A);
        do("Call")
    
        ActionClicker.backToLocal()
        wait(3)
        do("Answer")
		
        wait(5)
        self.io.loadFile(os.getcwd() + "./test-data/weekday1.wav")
        self.io.playRecord(os.getcwd() + "./outputs/test1.wav")

        output = AudioRecognizer.work(os.getcwd() + "./outputs/test1.wav")

        TextComparer.compareOutputToFile("./test-data/weekday1.txt", output)

        do("EndCall")

    def test_outgoing_call(self):
        wait(5)

        ActionClicker.dial(END_B)
        do("Call")
    
        wait(2)

        ActionClicker.switchToRemote(NUM_ENDS,0)

        do("Answer")
		
        ActionClicker.backToLocal()
        
        wait(2)
        self.io.loadFile(os.getcwd() + "./test-data/weekday1.wav")
        self.io.playRecord(os.getcwd() + "./outputs/test2.wav")

        output = AudioRecognizer.work(os.getcwd() + "./outputs/test2.wav")

        TextComparer.compareOutputToFile("./test-data/weekday1.txt", output)

        do("EndCall")


    def test_mute(self):
        wait(5)
        
        ActionClicker.dial(END_B);
        do("Call")
    
        wait(2)

        ActionClicker.switchToRemote(NUM_ENDS,0)

        do("Answer")
		
        ActionClicker.backToLocal()
        
        do("Mute")

        wait(2)
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
        wait(5)
        
        ActionClicker.dial(END_B)
        do("Call")
    
        wait(2)

        ActionClicker.switchToRemote(NUM_ENDS,0)

        do("Answer")
		
        ActionClicker.backToLocal()
        wait(2)

        do("Hold")

        wait(2)
        self.io.loadFile(os.getcwd() + "./test-data/weekday1.wav")
        self.io.playRecord(os.getcwd() + "./outputs/mute1.wav")

        output = AudioRecognizer.work(os.getcwd() + "./outputs/mute1.wav")
        print(TextComparer.isBlank(output))

        wait(2)

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
        do("ClearContactSearch")
        do("ContSearch")
        ActionClicker.type(END_B_NAME)
        do("VideoCall1")
        
        ActionClicker.switchToRemote(NUM_ENDS, 0)
        
        wait(3)
        
        do("VideoAccept")
        
        ActionClicker.backToLocal()
        
        wait(10)
        
        do("Center")
        
        wait(1)
        
        offset = ScreenScanner.verifyVideo()
        
        do("EndVideo")
        wait(5)
        do("ClearContactSearch")
        
    def video_upgrade(self):
        wait(5)
        ActionClicker.switchToRemote(NUM_ENDS,0)
        ActionClicker.dial(END_A);
        do("Call")
    
        ActionClicker.backToLocal()
        wait(3)
        do("Answer")
        wait(2)
        do("UpgradeVideo")
        ActionClicker.switchToRemote(NUM_ENDS,0)
        do("UpgradeVideo")
        
        ActionClicker.backToLocal()
        wait(8)
        
        offset = ScreenScanner.verifyVideo()
        
        do("EndVideo")
      #TODO must add logic for attended transfers
    def receive_transfer(self, transferType):
        wait(5)

        ActionClicker.switchToRemote(NUM_ENDS,1)

        ActionClicker.dial(END_B)
        do("Call")

        wait(2)
        
        ActionClicker.backToLocal()
        ActionClicker.switchToRemote(NUM_ENDS,0)
        do("Answer")
        
        wait(4)
        
        ActionClicker.backToLocal()
        ActionClicker.switchToRemote(NUM_ENDS,1)
        
        wait(4)
        
        ActionClicker.transfer(END_A, transferType)
        
        ActionClicker.backToLocal()
        
        wait(3)
        
        do("Answer")
        
        self.test_audio()
        
        do("EndCall")
    #TODO Add conference call   
    def call_swap(self):
        wait(5)

        ActionClicker.switchToRemote(NUM_ENDS,1)

        ActionClicker.dial(END_A)
        do("Call")

        wait(2)
        
        ActionClicker.backToLocal()
        
        wait(2)
        do("Answer")
        
        ActionClicker.switchToRemote(NUM_ENDS,0)
        ActionClicker.dial(END_A)
        do("Call")
        
        ActionClicker.backToLocal()
        
        wait(2)
        do("Answer2")
        wait(2)
        
        self.test_audio()
        
        do("Swap1")
        
        #self.test_audio()
        wait(2)
        
        do("Swap2")
        
        self.test_audio()
        
        do("EndVideo")
        
        wait(4)
        
        do("EndCall")
        
        do("EndVideo")
        
    #@TODO, fix this, not testing the right thing    
    def MWI(self):
        wait(5)

        ActionClicker.dial(END_B);
        do("Call")
    
        wait(2)

        ActionClicker.switchToRemote(NUM_ENDS,0)

        do("Answer")
		
        ActionClicker.backToLocal()
        
        wait(8)
        
        print(ScreenScanner.checkForImage("MWI", self.briaArea))
        
        do("EndCall")

    
    def contactCall(self):
        wait(5)
        
        do("Contacts")
        do("ContSearch")
        ActionClicker.type(END_B_NAME)
        do("ContactCall1")
        
        ActionClicker.switchToRemote(NUM_ENDS, 0)
        
        wait(3)
        
        do("Answer")
        
        ActionClicker.backToLocal()
        
        self.test_audio()

        do("EndCall")
        
        do("ClearContactSearch")     
   
   
    def historyCall(self):
        wait(5)
        
        do("HistoryTab")
        do("HistoryCall1")
        
        ActionClicker.switchToRemote(NUM_ENDS, 0)
        
        wait(3)
        
        do("Answer")
        
        ActionClicker.backToLocal()
                
        wait(1)
        
        self.test_audio()
        
        do("EndCall")
        
   
    def verifyPresence(self):
        wait(5)

        print(ScreenScanner.checkForImage("p2"))

        ActionClicker.dial(END_B);
        do("Call")
    
        wait(2)

        ActionClicker.switchToRemote(NUM_ENDS,0)

        do("Answer")
		
        ActionClicker.backToLocal()

        print(ScreenScanner.checkForImage("p3"))
        
        do("EndCall")
        
    def createContact(self, testNo):
        wait(5)
        
        do("Contacts")
        do("AddContact")
        do("ContactDisplay")
        ActionClicker.type("Display Test " + str(testNo))
        do("ContactFirstName")
        ActionClicker.type(str(testNo) + " First")
        do("ContactLastName")
        ActionClicker.type(str(testNo) +" Last")
        do("ContactSoftphone")
        ActionClicker.type("1112123124")
        do("ContactAddNum")
        do("SaveContact")
        
        wait(1)
        do("ClearContactSearch")
        
        do("ContSearch")
        ActionClicker.type(str(testNo))
        
        print(ScreenScanner.checkForImage("ContactExists"))
        
        do("ClearContactSearch")
        
    def verifyMissedCall(self):
        wait(5)
        do("HistoryTab")
        do("Dialpad")
        
        ActionClicker.switchToRemote(NUM_ENDS, 0)
        
        ActionClicker.dial(END_A);
        do("Call")
        
        ActionClicker.backToLocal();
        
        wait(20)
        
        print(ScreenScanner.checkForImage("1MissedCall"))
        
        
    def contactPresence(self):
        wait(5)
        
        ActionClicker.switchToRemote(NUM_ENDS, 0)
        
        do("SetPresenceBusy")
        
        ActionClicker.backToLocal()
        
        do("Contacts")
        do("ContSearch")
        ActionClicker.type(END_B_NAME)
        
        print(ScreenScanner.checkForImage("ContactBusyPresence"))
        
        ActionClicker.switchToRemote(NUM_ENDS, 0)
        
        do("SetPresenceAvailable")
        
        ActionClicker.backToLocal()
        
        do("ClearContactSearch")
        
    def receiveIM(self):
        wait(5)
        
        ActionClicker.switchToRemote(NUM_ENDS, 0)
        
        #do("GoToMessageSearch")
        do("Contacts")
        do("ContSearch")
        
        ActionClicker.type(END_A_NAME)
        
        do("MessageTopContact")
        
        #do("MessageTopIMResult")
        
        ActionClicker.type("i", time=0.1)
        ActionClicker.pressKey('enter')
        ActionClicker.type("i", time=0.1)
        ActionClicker.pressKey('enter')
        ActionClicker.type("i", time=0.1)
        ActionClicker.pressKey('enter')
        ActionClicker.type("i", time=0.1)
        ActionClicker.pressKey('enter')
        ActionClicker.type("test", time=0.1)
        ActionClicker.pressKey('enter')
        
        do("ClearContactSearch")
        
        ActionClicker.backToLocal()
        
        wait(2)
        
        do("Contacts")
        do("ContSearch")
        
        ActionClicker.type(END_B_NAME)
        
        do("MessageTopContact")
        wait(2)
        print(ScreenScanner.checkForImage("testImg"))
        
        do("ClearContactSearch")
        
    def call_recording(self):
        wait(5)

        ActionClicker.dial(END_B);
        do("Call")
    
        wait(2)

        ActionClicker.switchToRemote(NUM_ENDS,0)

        do("Answer")
		
        ActionClicker.backToLocal()
        
        do("toggleTopCallRecording")
        
        wait(2)
        self.io.loadFile(os.getcwd() + "./test-data/weekday1.wav")
        self.io.play(os.getcwd() + "./test-data/weekday1.wav")

        do("toggleTopCallRecording")
		
        wait(3)
        
        do("EndCall")

        wait(2)

        output = AudioRecognizer.work(RECORDING_PATH + '/' + AudioRecognizer.findNewestRecording(RECORDING_PATH))

        TextComparer.compareOutputToFile("./test-data/weekday1.txt", output)

    def send_log(self, testNo):
        do("ToSendLogReportTxt")
        ActionClicker.type("This is a test log send by an automated script. Is test number " + testNo)

        do("SendReport")

        ScreenScanner.checkForImage("LogSent")
		
    def check_user_portal(self):
        do("UserPortalTab")

        ScreenScanner.checkForImage("UserPortal")


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
        
        wait(2)
        
        ScreenScanner.checkForImage("PrivateChat")
        
        do("DeleteTopRoom")
        
    def public_chatroom(self):
        do("GoToCreateChat")

        do("ChatRoomPublic")
        
        do("SetChatRoomName")
        
        ActionClicker.type("Public")
        
        do("CreateChatRoom")
        
        wait(2)
        
        ScreenScanner.checkForImage("PublicChat")
        
        do("DeleteTopRoom")
    
    def host_screen_share(self):
        
        do("Contacts")
        do("ContSearch")
        ActionClicker.type(END_B_NAME)
        
        do("StartScreenShare")
        
        ActionClicker.switchToRemote(NUM_ENDS, 0)
        
        area = ScreenScanner.findImage("JoinScreenshare")
        
        ActionClicker.clickAt(area)
        
        wait(2)
        
        print(ScreenScanner.checkForImage("SmallScreenShareImage"))
        
        do("CloseScreenShare")
        
        ActionClicker.backToLocal()
        
        do("EndScreenShare")
        
        do("ClearContactSearch")