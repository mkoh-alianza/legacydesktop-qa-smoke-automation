sys.path.append('..')
sys.path.append('./objects')
from constants import *
from test_agent import TestAgent


ts = TestAgent()

ts.test_incoming_call()