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
                sleep(coords[j][2])
            
            pyautogui.moveTo(coords[j][0], coords[j][1])
            pyautogui.mouseDown(button=coords[j][3])
            pyautogui.mouseUp(button=coords[j][3])
            
    def switchToRemote(num, pc):
        coords = []
        with open(os.getcwd() + './actions/remote.txt', 'r') as f:
            for line in f:
                coords.append(eval(line))
        
        offset = (-num / 2 * 275) + 137.5
        
        pyautogui.moveTo(coords[0][0], coords[0][1])
        pyautogui.mouseDown(button=coords[0][3])
        pyautogui.mouseUp(button=coords[0][3])
        sleep(1)



        pyautogui.moveTo(coords[0][0] + offset + (275 * pc), coords[0][1] - 100)
        pyautogui.mouseDown(button=coords[0][3])
        pyautogui.mouseUp(button=coords[0][3])


    def backToLocal():
        coords = []
        with open(os.getcwd() + './actions/local.txt', 'r') as f:
            for line in f:
                coords.append(eval(line))
                
        pyautogui.moveTo(coords[0][0], coords[0][1])
        pyautogui.mouseDown(button=coords[0][3])
        pyautogui.mouseUp(button=coords[0][3])
        sleep(1)