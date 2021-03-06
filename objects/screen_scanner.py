from PIL import ImageGrab
from PIL import Image

import pyautogui

import time

class ScreenScanner:

    def verifyEquals(grab, toFind, start, step=1):
        
        wrongCount = 0
        for x in range(0, toFind.width):
            for y in range(0, toFind.height):
                a = grab.getpixel((x + start[0], y + start[1]))
                b = toFind.getpixel((x,y))
                for i in range(0, 3):
                    if((a[i] - 20 > b[i]) or (a[i] + 20 < b[i])):
                        return False
        
        return True
                    
    
    def findImage(toFind, area=None):
        
        try:
            return  pyautogui.locateCenterOnScreen("./ScannerImages/" + toFind + ".png", confidence=0.9)
        except:
            return False
                    

    
    def checkForImage(toFind , area=None):
        
        try: 
            dest = pyautogui.locateCenterOnScreen("./ScannerImages/" + toFind + ".png", confidence=0.9)
            if(dest == None):
                return False
            else:
                return True
            
        except:
            return False
        

    def findBria():

        try: 
            dest = pyautogui.locateCenterOnScreen("./ScannerImages/" + toFind + ".png", confidence=0.9)
            if(dest == None):
                return None
            else:
                return dest
            
        except:
            return None
        

    def verifyVideo():
        grab = ImageGrab.grab()
        a = grab.getpixel((567, 273))
        

        time.sleep(6)
        grab = ImageGrab.grab()
        b = grab.getpixel((567, 273))
        
        if(a[1] != b[1] or a[0] != b[0]):
            print("Video Verified")
            
        
        '''
        grab = ImageGrab.grab()
        target = Image.open("./ScannerImages/videoWindowControls.png")
        for x in range(0, grab.width - target.width):
           for y in range(0, grab.height - target.height):
               print(x)
               print(y)
               if(ScreenScanner.verifyEquals(grab, target, (x,y))):
                    coords = (x + 322, y +20)
                    return coords
        
        #a = grab.getpixel(coords[0], coords[1] - 100)
        
        return None
        '''