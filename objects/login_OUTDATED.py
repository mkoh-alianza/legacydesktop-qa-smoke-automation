import time
import os
import platform
import subprocess
# pip install pynput
from pynput.keyboard import Key, Controller as KeyboardController
from pynput.mouse import Button, Controller as MouseController
# pip install psutil
import psutil
# pip install pywin32
import win32gui
import win32con
import win32com.shell.shell as shell 
import re
import shutil
import credentials

from screen_scanner import ScreenScanner


class Login: 

    def __init__(self, brandIndex = 0, credentials = credentials.vccs[0], printProgress = True):
        self.keyboard = KeyboardController()
        self.mouse = MouseController()
        self.os = os.name
        brandTypes = ["Bria Enterprise", "Cymbus"]
        self.brand = brandTypes[brandIndex]
        if brandIndex == 0:
            self.path = '"C:\Program Files (x86)\CounterPath\Bria Enterprise\BriaEnterprise.exe"'
        elif brandIndex == 1: 
            self.path = '"C:\Program Files (x86)\Cymbus\Cymbus\cymbus.exe"'
        self.proc = ""
        self.procPid = ""
        self.username = credentials[0]
        self.password = credentials[1]
        self.hwndMain = ""
        self.printProgress = printProgress


    def __mouseClick__(self, x, y):
        self.mouse.position = (x, y)
        self.mouse.press(Button.left)
        self.mouse.release(Button.left)


    # change user login credentials 
    def changeUser(self, credentials):
        self.username = credentials[0]
        self.password = credentials[1]
    

    def switchUser(self, credentials):
        self.__closeProcess__()
        self.changeUser(credentials)
        self.setup()


    # Search through processes to check if application is running
    # getProcId source: benchmark-testing 
    def __getProcId__(self):
        if self.printProgress:
            print("\nSearching for the process...")
        pidsList = psutil.pids()
        procPid = 'notFound'
        
        if self.brand == 'Cymbus':
            client_proc_name = 'cymbus.exe'
        else: 
            client_proc_name = 'BriaEnterprise.exe'

        for pid in pidsList:
            try:
                p = psutil.Process(pid)
                if(p.name() == client_proc_name):
                    if self.printProgress:
                        print("Process Found, Process ID = " + str(pid))
                    if(procPid != 'notFound'):
                        if self.printProgress:
                            print("WARNING: Multiple instances of " + client_proc_name + " found! May test the incorrect one...")
                        if(proc.memory_percent() < p.memory_percent()):
                            procPid = pid
                            proc = p
                    else:
                        procPid = pid
                        proc = p
            except:
                if self.printProgress:
                    print("Bypassing Access Exception...")

        if(procPid == 'notFound'):
            if self.printProgress:
                print(client_proc_name + " not found")
            return False 
        if self.printProgress:
            print("process ID to be used: " + str(procPid))
        self.procPid = procPid 
        return True 


    # Run application and login 
    def runApplication(self):
        # if application is not open 
        if not self.__getProcId__():
            if self.printProgress:
                print("Process not found, opening " + self.brand)
            self.proc = subprocess.Popen(self.path)
            time.sleep(6)
            self.procPid = self.proc.pid
        # if application is already open 
        else: 
            self.proc = psutil.Process(self.procPid) 
        # if not logged in, log in and bring it to front 
        if not self.__setWindow__(self.brand):
            self.__setWindow__(self.brand + " Sign In")
            self.__activateWindow__()
            self.login() 
            time.sleep(2)
            self.__setWindow__(self.brand)
        else:
            if self.printProgress: 
                print("Already logged into " + self.brand)
        

    # Find and store application window information 
    def __setWindow__(self, windowName):
        if self.os == "nt": 
            self.hwndMain = win32gui.FindWindow(None, windowName)
            if self.hwndMain:
                if self.printProgress:
                    print("Set hwndMain to " + windowName)
                return True
            return False
            if self.printProgress:
                print("Failed to set hwndMain to " + windowName)
        elif self.os == "posix": 
            # ---------TODO---------- find window and set self.hwndMain 
            print("")


    # Bring application window to the front 
    def __activateWindow__(self):
        if self.printProgress:
            print("Bringing " + self.brand + " to front")
        if self.os == "nt":
            win32gui.ShowWindow(self.hwndMain, win32con.SW_RESTORE)
            win32gui.ShowWindow(self.hwndMain, win32con.SW_SHOWNORMAL)
            win32gui.ShowWindow(self.hwndMain, win32con.SW_SHOW)
            win32gui.SetForegroundWindow(self.hwndMain)
        elif self.os == "posix": 
            # ---------TODO---------- activate window for mac 
            print("")


    # Move the application window to the top left corner 
    # --Currently size is set to [318, 530]
    def __moveWindow__(self):
        if self.printProgress:
            print("Now moving " + self.brand + " to the left corner")
        if self.os == "nt": 
            if re.match("10.0.22000", platform.version()):
                win32gui.MoveWindow(self.hwndMain, 0, 0, 318, 530, True)
            elif re.match(r"10\.0\.\d*", platform.version()):
                win32gui.MoveWindow(self.hwndMain, -7, 0, 318, 530, True)
            else:
                win32gui.MoveWindow(self.hwndMain, 0, 0, 318, 530, True)
        # ---------TODO---------- set window size and location for mac
        elif self.os == "posix": 
            print("")


    def __closeProcess__(self):
        # Search through processes and terminate running instances
        if self.printProgress:
            print("Searching through the process to terminate...")
        pidsList = psutil.pids()
        
        if self.brand == 'Cymbus':
            client_proc_name = 'cymbus.exe'
        else: 
            client_proc_name = 'BriaEnterprise.exe'

        for pid in pidsList:
            try:
                p = psutil.Process(pid)
                if(p.name() == client_proc_name):
                    if self.printProgress:
                        print("Process found, terminating process ID = " + str(pid))
                    p.terminate()
            except:
                if self.printProgress:
                    print("Bypassing Access Exception...")


    # Log in 
    def login(self):
        if self.printProgress:
            print("Loggin in...")
        time.sleep(1)
        # move cursor to username
        self.keyboard.press(Key.tab)
        self.keyboard.release(Key.tab)
        # type in username
        self.keyboard.type(self.username)
        self.keyboard.press(Key.tab)
        self.keyboard.release(Key.tab)
        # move cursor to password
        # type in password
        self.keyboard.type(self.password)
        self.keyboard.press(Key.enter)
        self.keyboard.release(Key.enter)
        time.sleep(5)
        # Close Emergency Location Update prompt if it shows up 
        location = ScreenScanner.findImage('CymbusPrompt')
        if location:
            self.__mouseClick__(location[0] + 507, location[1] + 229)



    # Function to run application, bring it to front, then move it to the corner  
    def setup(self):
        self.runApplication()
        self.__activateWindow__()
        self.__moveWindow__()


    # Log out using mouse clicks
    def logout_mouse(self):
        self.__setWindow__(self.brand)
        self.__activateWindow__()
        if self.printProgress:
            print("Now logging out of " + self.brand)
        self.__mouseClick__(36, 44)
        time.sleep(1)
        self.__mouseClick__(40, 112)
        


    # Exit using mouse clicks
    def close_mouse(self):
        if not self.__setWindow__(self.brand):
            self.__setWindow__(self.brand + " Sign In")
            self.__activateWindow__()
            if self.printProgress:
                print("Now closing " + self.brand)
            location = ScreenScanner.findImage('CymbusSignIn')
            self.__mouseClick__(location[0] + 30, location[1] + 50)
        else:
            self.__activateWindow__()
            if self.printProgress:
                print("Now closing " + self.brand)
            self.__mouseClick__(36, 44)
            time.sleep(1)
            self.__mouseClick__(28, 143)


    # Log out using alt+s s shortcut 
    def logout_keyboard(self):
        self.__setWindow__(self.brand)
        self.__activateWindow__()
        if self.printProgress:
            print("Now logging out of " + self.brand)
        self.keyboard.press(Key.alt)
        self.keyboard.press("s")
        self.keyboard.release("s")
        self.keyboard.release(Key.alt)
        self.keyboard.press("s")
        self.keyboard.release("s")


    # Exit using ctrl+q
    def close_keyboard(self):
        if not self.__setWindow__(self.brand):
            self.__setWindow__(self.brand + " Sign In")
        self.__activateWindow__()
        if self.printProgress:
            print("Now closing " + self.brand)
        self.keyboard.press(Key.ctrl)
        self.keyboard.press("q")
        self.keyboard.release(Key.ctrl)
        self.keyboard.release("q")





class Installer: 

    def __init__(self, brandIndex = 0, printProgress=False):
        self.keyboard = KeyboardController()
        self.mouse = MouseController()
        self.os = os.name
        brandTypes = ["Bria Enterprise", "Cymbus"]
        self.brand = brandTypes[brandIndex]
        if brandIndex == 0:
            self.path = '"C:\Program Files (x86)\CounterPath\Bria Enterprise\BriaEnterprise.exe"'
        elif brandIndex == 1: 
            self.path = '"C:\Program Files (x86)\Cymbus\Cymbus\cymbus.exe"'
        self.printProgress = printProgress


    def __mouseClick__(self, x, y):
        self.mouse.position = (x, y)
        self.mouse.press(Button.left)
        self.mouse.release(Button.left)


    def clearCache(self):
        if self.os == "nt": 
            if self.brand == "Cymbus":
                CymbusTemp = os.path.expandvars(r'%APPDATA%\..\Local\Temp\Cymbus') 
                if os.path.exists(CymbusTemp):
                    shutil.rmtree(CymbusTemp)
                    if self.printProgress:
                        print("removed " + CymbusTemp)
                CymbusRoaming = os.path.expandvars(r'%APPDATA%\Cymbus')
                if os.path.exists(CymbusRoaming):
                    shutil.rmtree(CymbusRoaming)
                    if self.printProgress:
                        print("removed " + CymbusRoaming)
            else: 
                EnterpriseTemp = os.path.expandvars(r'%APPDATA%\..\Local\Temp\CounterPath Corporation')
                if os.path.exists(EnterpriseTemp):
                    shutil.rmtree(EnterpriseTemp)
                    if self.printProgress:
                        print("removed " + EnterpriseTemp)
                EnterpriseRoaming = os.path.expandvars(r'%APPDATA%\CounterPath')
                if os.path.exists(EnterpriseRoaming):
                    shutil.rmtree(EnterpriseRoaming)
                    if self.printProgress:
                        print("removed " + EnterpriseRoaming)
                EnterpriseRoaming2 = os.path.expandvars(r'%APPDATA%\CounterPath Corporation')
                if os.path.exists(EnterpriseRoaming2):
                    shutil.rmtree(EnterpriseRoaming2)
                    if self.printProgress:
                        print("removed " + EnterpriseRoaming2)
        elif self.os == "posix": 
        # ---------TODO---------- delete cache for mac
            if self.printProgress:
                print("")
    


    def __closeProcess__(self):
        # Search through processes and terminate running instances
        if self.printProgress:
            print("Searching through the process to terminate...")
        pidsList = psutil.pids()
        
        if self.brand == 'Cymbus':
            client_proc_name = 'cymbus.exe'
        else: 
            client_proc_name = 'BriaEnterprise.exe'

        for pid in pidsList:
            try:
                p = psutil.Process(pid)
                if(p.name() == client_proc_name):
                    if self.printProgress:
                        print("Process found, terminating process ID = " + str(pid))
                    p.terminate()
            except:
                if self.printProgress:
                    print("Bypassing Access Exception...")



    def uninstall(self):
        self.__closeProcess__()
        if self.printProgress:
            print("Uninstalling " + self.brand + "...")
        if self.os == "nt":
            command = 'wmic product where name="%s" call uninstall' % self.brand
            shell.ShellExecuteEx(lpVerb='runas', lpFile='cmd.exe', lpParameters='/c '+ command)
        elif self.os == "posix":
            print("")
        time.sleep(20)



    def install(self):
        self.__closeProcess__()
        if self.printProgress:
            print("Installing " + self.brand + "...")

        # ---------TODO---------- Change how we get this file path, it's hardcoded now since we don't have gui
        if self.os == "nt":
            if self.brand == "Cymbus":
                filepath = r"C:\Users\QA\Downloads\Builds\Cymbus_6.5.3_RC1_109972.msi"
            else:
                filepath = r"C:\Users\QA\Downloads\Builds\Bria_Enterprise_6.5.3_RC1_109968.msi"
            self.proc = subprocess.Popen('msiexec /i %s /n' % filepath, shell=True)
            if self.printProgress:
                print('Running msi to install ' + self.brand)

            if self.brand == "Cymbus":
                time.sleep(1)
                location = ScreenScanner.findImage('CymbusSetup')
                if not location:
                    raise ValueError("Image 'CymbusSetup' not found on screen")
                self.__mouseClick__(location[0] + 328, location[1] + 357)
                # check if Cymbus is already installed
                location = ScreenScanner.findImage('Repair')
                if location:
                    if self.printProgress:
                        print("%s already installed, going to repair" % self.brand)
                    self.mouse.position = (location[0] + 50, location[1] + 10)
                    location = ScreenScanner.findImage('Repair')
                    self.mouse.position = (location[0] + 50, location[1] + 10)
                else:
                    if self.printProgress:
                        print("%s not installed, going to install" % self.brand)
                    location = ScreenScanner.findImage('CymbusLicenseAgreement')
                    self.mouse.position = (location[0] + 5, location[1] + 5)
                    location = ScreenScanner.findImage('CymbusInstall')
                    self.mouse.position = (location[0] + 20, location[1] + 10)
                if self.printProgress:
                    print("Authorization required, please allow %s to make changes" % self.brand)
                time.sleep(20)
                location = ScreenScanner.findImage('CymbusFinish')
                self.mouse.position = (location[0] + 20, location[1] + 10)
            else:
                time.sleep(20)

        elif self.os == "posix":
            if self.printProgress:
                print("")

        if self.printProgress:
            print("Finished Installing %s!" % self.brand)



    def cleanInstall(self):
        self.clearCache()
        self.uninstall()






if __name__ == '__main__':
    # login = Login(1)
    # login.setup()
    # time.sleep(12)
    # login.close_mouse()

    # time.sleep(10)

    # login = Login(0, credentials.ptt[1], True)
    # login.setup()
    # time.sleep(12)
    # login.close()
    
    
    installer = Installer(1, True)
    # installer.uninstall()
    installer.install()