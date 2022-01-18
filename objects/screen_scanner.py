from PIL import ImageGrab
from PIL import Image

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
                    

    def checkForImage(toFind , area=None):
        
        grab = ImageGrab.grab(bbox = area)
        target = Image.open("./ScannerImages/" + toFind)
        
        for x in range(0, grab.width - target.width):
            for y in range(0, grab.height - target.height):
                if(ScreenScanner.verifyEquals(grab, target, (x,y))):
                    return True
                    
        return False

    def findBria():
        
        grab = ImageGrab.grab()
        target = Image.open("./ScannerImages/Title.png")
        found1 = False
        
        for x in range(0, grab.width - target.width):
            for y in range(0, grab.height - target.height):
                if(ScreenScanner.verifyEquals(grab, target, (x,y))):
                    if(found1 == False):
                        x1y1 = (x,y)
                        target = Image.open("./ScannerImages/Bottom.png")
                        found1 = True
                    else:
                        x2y2 = (x + target.width, y + target.height)
                        return x1y1 + x2y2
                    
                    
        return None

    def verifyVideo():
        grab = ImageGrab.grab()
        a = grab.getpixel((567, 273))
        
        grab = ImageGrab.grab()
        time.sleep(6)
        b = grab.getpixel((567, 273))
        
        #if(a[1] != b[1] or a[0] != b[0]):
            #print("Video Verified")
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