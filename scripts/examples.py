import sys
sys.path.append('..')
sys.path.append('./objects')
from constants import *
from test_agent import TestAgent


ts = TestAgent()

#Sets up a Contact Call here by going to contacts, searching up end b, calling them
do("Contacts")
do("ContSearch")
ActionClicker.type(END_B_NAME)
do("ContactCall1")
ActionClicker.switchToRemote(NUM_ENDS, 0)
wait(3)
do("Answer")
ActionClicker.backToLocal()

#Now that it is in a call with end B, we can verify audio
ts.test_audio()