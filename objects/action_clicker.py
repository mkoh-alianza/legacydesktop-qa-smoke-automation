import pyautogui
from time import sleep
import os

class ActionClicker:
    
    
    '''Does the given action, the offset is from the top left, see 'action definitions' file for more info '''
    def doAction(action, offset=None):
        coords =[]
        with open(os.getcwd() + "./actions/"  + action + '.txt', 'r') as f:
            for line in f:
                coords.append(eval(line))
        
        if(offset):
            diff = offset
        else:
            diff = (0,0)
        
        for j in range(0, len(coords)):
            if(j != 0):
                sleep(coords[j][2])
            
            pyautogui.moveTo(coords[j][0] + diff[0], coords[j][1] + diff[1])
            pyautogui.mouseDown(button=coords[j][3])
            pyautogui.mouseUp(button=coords[j][3])
            
    ''''''       
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

    def type(txt, time=0.25):
        pyautogui.write(txt, interval = time)

    def pressKey(key):
        pyautogui.press(key)

    def backToLocal():
        coords = []
        with open(os.getcwd() + './actions/local.txt', 'r') as f:
            for line in f:
                coords.append(eval(line))
                
        pyautogui.moveTo(coords[0][0], coords[0][1])
        pyautogui.mouseDown(button=coords[0][3])
        pyautogui.mouseUp(button=coords[0][3])
        sleep(1)
    
    def clickAt(xy, buttonPress = 'left'):
        if(xy == None):
            return False
    
        pyautogui.moveTo(xy.x, xy.y)
        pyautogui.mouseDown(button=buttonPress)
        pyautogui.mouseUp(button=buttonPress)
    
    
    def dial(num):
        ActionClicker.doAction("DialPad")
        for digit in num:
            ActionClicker.doAction("Dial" + digit)
            
    def transfer(num, transfer):
       ActionClicker.doAction("TransferStartDial")
       ActionClicker.type(num)
       ActionClicker.doAction(transfer)
       
        