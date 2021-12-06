
sys.path.append('./objects')

from test_agent import TestAgent


agent = TestAgent(WEBSOCKET_ADDRESS)

agent.two_point_zero_one_B()

