import sys 
import time
import os
from os.path import exists
import platform
import re           # for regex
import pyautogui    # pip install opencv-python
import win32com.shell.shell as shell    # for running in admin mode
import ctypes # for running in admin mode

from initializer import Initializer
from credentials import accountDict
from installer_click import Click_Installer

from PIL import Image 





class Login: 

    def __init__(self, initializer, installer):
        self.os = os.name
        self.printProgress = initializer.printProgress
        self.installerPath = initializer.installerPath
        self.imageFolder = './../detectorImages/'
        self.scaleRatio = initializer.scaleRatio
        self.brand = initializer.brand
        self.exePath = initializer.exePath
        self.account = initializer.account 
        self.username = accountDict[self.account][0]
        self.username = accountDict[self.account][1]
        self.installer = installer 
        




    def __imageLocation__(self, filename, center=False, confidence=0.6):
        try: 
            image = Image.open(self.imageFolder + filename + '.png')
            image = image.resize( [int(self.scaleRatio * s) for s in image.size] )
        except FileNotFoundError:
            if self.printProgress: print(f"Image file '{filename}' does not exist")
            raise ValueError

        try: 
            if center: 
                loc_size = pyautogui.locateCenterOnScreen(image, confidence=confidence)
            else: 
                loc_size = pyautogui.locateOnScreen(image, confidence=confidence)
            return loc_size 
        except pyautogui.ImageNotFoundException: 
            if self.printProgress: print(f"{filename} not found on screen")
            return False 
        

    def __clickImageCenter__(self, filename, button='left', confidence=0.6):
        loc_size = self.__imageLocation__(filename=filename, center=True, confidence=confidence)
        if not loc_size: return False 
        pyautogui.click(x=loc_size[0], y=loc_size[1], button=button)
        return True 


    def __clickXY__(self, x, y, button='left', clicks=1):
        pyautogui.click(x=x, y=y, button=button, clicks=clicks)





    # change user login credentials 
    def changeUser(self, credentials):
        self.username = credentials[0]
        self.password = credentials[1]
    

    def switchUser(self, credentials):
        self.__closeProcess__()
        self.changeUser(credentials)
        self.setup()



    # Run application and login 
    def runApplication(self):
        print("")
        

    def showPhone(self):
        if self.printProgress: print("Trying to bring main window to the front")
        try: 
            self.__clickImageCenter__(f"{self.brand}Icon_Corner", button='right')
            self.__clickImageCenter__("Icon_Corner_Show")
        except:
            if self.__clickImageCenter__("Icon_Corner_Signin"): print("Not logged in")
            else: print("Unable to show the phone")
            raise ValueError
    


    # Log in 
    def login(self):
        if self.printProgress: print("Closing application and clearing cache")
        self.installer.clearCache() 
        if self.printProgress: print(f"Opening {self.brand}...")
        self.__clickImageCenter__(f"{self.brand}Icon")
        time.sleep(7)
        if self.printProgress: print("Logging in...")
        if self.__imageLocation__(f"Login_{self.brand}"):
            usernameX, usernameY = self.__imageLocation__(filename="Login_Username", center=True, confidence=0.9)
            passwordX, passwordY = self.__imageLocation__(filename="Login_Password", center=True, confidence=0.9)
        else: 
            print(f"Login page for {self.brand} not detected on screen, exiting")
            raise ValueError
        for account in accountDict[self.account]:
            self.__clickXY__(usernameX, usernameY, 'left')
            pyautogui.hotkey("ctrl", "a")
            pyautogui.write(account[0])
            self.__clickXY__(passwordX, passwordY, 'left')
            pyautogui.hotkey("ctrl", "a")
            pyautogui.write(account[1])
            self.__clickImageCenter__(f"Login_{self.brand}SignIn")
            time.sleep(3)
            if not self.__imageLocation__(f"Login_{self.brand}"):
                self.username = account[0]
                self.username = account[1]
                if self.printProgress: print(f"Logged in using account {self.username}\n")
                break 
            if account == accountDict[self.account][-1]:
                print("None of the accounts in the specified server worked, exiting")
                raise ValueError



    # exit using mouse clicks
    def exit(self):
        self.showPhone()
        if self.__imageLocation__("Menu"):
            self.__clickImageCenter__("Menu_Softphone")
            time.sleep(1)
            self.__clickImageCenter__("Softphone_Exit")
        
    # sign out using mouse clicks
    def signout(self):
        self.showPhone()
        if self.__imageLocation__("Menu"):
            self.__clickImageCenter__("Menu_Softphone")
            time.sleep(1)
            self.__clickImageCenter__("Softphone_Signout")


    # # Exit using mouse clicks
    # def close(self):
    #     if not self.__setWindow__(self.brand):
    #         self.__setWindow__(self.brand + " Sign In")
    #         self.__activateWindow__()
    #         if self.printProgress: print(f"Now closing {self.brand}")
    #         location = ScreenScanner.findImage('CymbusSignIn')
    #         self.__mouseClick__(location[0] + 30, location[1] + 50)
    #     else:
    #         self.__activateWindow__()
    #         if self.printProgress: print(f"Now closing {self.brand}")
    #         self.__mouseClick__(36, 44)
    #         time.sleep(1)
    #         self.__mouseClick__(28, 143)




    






if __name__ == '__main__':

    def is_admin():
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False

    if is_admin():
        
        try: 
            initializer = Initializer()
            installer = Click_Installer(initializer)
            login = Login(initializer, installer)
            # login.signout()
            login.login()
            
            input("\nNo issues, press enter to exit!")
        except Exception:
            input("\nPress Enter to exit...")
        except KeyboardInterrupt:
            input("\nKeyboard Interrupt detected, press Enter to exit...")


    else:
        # Re-run the program with admin rights
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
        exit(0)