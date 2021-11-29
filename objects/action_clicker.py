import pyautogui
from time import sleep
import os

class ActionClicker:
    
    def __init__(self, source):
        self.totalEnds
        
    def doAction(action):
        coords =[]
        with open(os.getcwd() + "./actions/"  + action + '.txt', 'r') as f:
            for line in f:
                coords.append(eval(line))
        
        
        for j in range(0, len(coords)):
            if(j != 0):
                time.sleep(coords[j][2])
            
            pyautogui.moveTo(coords[j][0], coords[j][1])
            pyautogui.mouseDown(button=coords[j][3])
            pyautogui.mouseUp(button=coords[j][3])
            
    def switchToRemote(self, pc):
        os.getcwd() + './actions/remote.txt', 'r') as f:
            for line in f:
                coords.append(eval(line))
        
        offset = (self.totalEnds / 2 * 40) + 20
        
        
        pyautogui.moveTo(coords[0][0], coords[0][1])
        pyautogui.mouseDown(button=coords[0][3])
        pyautogui.mouseUp(button=coords[0][3])
        time.sleep(1)
        
        pyautogui.moveTo(coords[0][0] - offset + pc * 40, coords[0][1] + 40)
        pyautogui.mouseDown(button=coords[0][3])
        pyautogui.mouseUp(button=coords[0][3])