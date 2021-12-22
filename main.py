import sys


sys.path.append('./objects')
from constants import *
from test_agent import TestAgent


agent = TestAgent(WEBSOCKET_ADDRESS)

agent.io_setup()
agent.test_incoming_call()
agent.test_outgoing_call()
agent.test_mute()
agent.test_hold()

