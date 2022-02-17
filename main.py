import sys


sys.path.append('./objects')
from constants import *
from test_agent import TestAgent
from screen_scanner import ScreenScanner
from action_clicker import ActionClicker


ts = TestAgent()

ts.test_incoming_call()

ts.test_outgoing_call()

ts.test_mute()

ts.test_hold()

ts.speaker_mode()

ts.video_start()

ts.video_upgrade()

ts.recieve_transfer()

ts.call_swap()

ts.MWI()

ts.contactCall()

ts.historyCall()

ts.verifyPresence()

ts.createContact(1)

ts.verifyMissedCall()

ts.contactPresence()

ts.reveiveIM()

ts.call_recording()

ts.send_log(1)

ts.check_user_portal()

ts.check_uem_vqm()

ts.check_uem_analytics()

ts.private_chatroom()

ts.public_chatroom()

ts.host_screen_share()