import sys
sys.path.append('..')
sys.path.append('./objects')
from constants import *
from test_agent import TestAgent


ts = TestAgent()

# ------------ Example 1 -----------------
#Simple 'test incoming call'
ts.test_incoming_call()
ts.wait(6)


# ------------ Example 2 ------------------
#A call specifically through contacts
#Sets up a Contact Call here by going to contacts, searching up end b, calling them
ts.do("Contacts")
ts.do("ContSearch")
ts.typeText(END_B_NAME)
ts.do("ContactCall1")
ts.switchToRemote(NUM_ENDS, 0)
ts.wait(3)
ts.do("Answer")
ts.backToLocal()

#Now that it is in a call with end B, we can verify audio
result = ts.test_audio()
ts.log(result, '1.10')

# ------------ Example 3 ------------------
#First, receiving a call from a remote end

ts.ActionClicker.switchToRemote(NUM_ENDS, 0)
        
ts.ActionClicker.dial(END_A)
ts.do("Call")
        
ts.backToLocal()
#Waiting for the call to time out
        
wait(20)
                
#Now, checking for the "1MissedCall" Image        
        
print(ts.find("1MissedCall"))