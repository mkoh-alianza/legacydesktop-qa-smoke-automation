import sys

sys.path.append('./objects')


sys.path.append('./objects')
from constants import *
from test_agent import TestAgent
from screen_scanner import ScreenScanner
print("Enter the file name of the png to search for:")
x = input()
print(ScreenScanner.checkForImage(x))

'''
agent = TestAgent(WEBSOCKET_ADDRESS)

<<<<<<< Updated upstream
agent.io_setup()
agent.test_incoming_call()
agent.test_outgoing_call()
agent.test_mute()
agent.test_hold()

=======
agent.two_point_zero_one_B()
'''

