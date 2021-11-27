import pyautogui
from time import sleep
import os

class ActionClicker:
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
            