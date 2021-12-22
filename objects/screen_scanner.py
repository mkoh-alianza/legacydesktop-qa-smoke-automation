from PIL import ImageGrab
from PIL import Image

class ScreenScanner:

    def verifyEquals(grab, toFind, start):
        
        for x in range(0, toFind.width):
            for y in range(0, toFind.height):
                a = grab.getpixel((x + start[0], y + start[1]))
                b = toFind.getpixel((x,y))
                for i in range(0, 3):
                    if((a[i] - 4 > b[i]) or (a[i] + 4 < b[i])):
                        return False
        
        return True
                    

    def checkForImage(toFind , area=None):
        
        grab = ImageGrab.grab(bbox = area)
        target = Image.open(toFind)
        
        for x in range(0, grab.width - target.width):
            for y in range(0, grab.height - target.height):
                if(ScreenScanner.verifyEquals(grab, target, (x,y))):
                    return True
                    
        return False

    def findBria():
        
        grab = ImageGrab.grab()
        target = Image.open("Title.png")
        found1 = False
        
        for x in range(0, grab.width - target.width):
            for y in range(0, grab.height - target.height):
                if(verifyEquals(grab, target, (x,y))):
                    if(found1 == False):
                        x1y1 = (x,y)
                        target = Image.open("Bottom.png")
                        found1 = True
                    else:
                        x2y2 = (x + target.width, y + target.height)
                        return x1y1 + x2y2
                    
                    
        return False
