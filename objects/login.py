import time
import os
import platform
import subprocess
# pip install pynput
from pynput.keyboard import Key, Controller
# pip install psutil
import psutil
# pip install pywin32
import win32gui
import win32con
import win32com.shell.shell as shell 
import re
import shutil
import credentials


class Login: 

    def __init__(self, brandIndex = 0, credentials = credentials.vccs[0]):
        self.keyboard = Controller()
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


    # change user login credentials 
    def changeUser(self, credentials):
        self.username = credentials[0]
        self.password = credentials[1]
        print("Changed login credentials")


    # Search through processes to check if application is running
    # getProcId source: benchmark-testing 
    def getProcId(self):
        print("Searching for the process...")
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
                    print("Process Found, Process ID = " + str(pid))
                    if(procPid != 'notFound'):
                        print("WARNING: Multiple instances of " + client_proc_name + " found! May test the incorrect one...")
                        if(proc.memory_percent() < p.memory_percent()):
                            procPid = pid
                            proc = p
                    else:
                        procPid = pid
                        proc = p
            except:
                print("Bypassing Access Exception...")

        if(procPid == 'notFound'):
            print(client_proc_name + " not found")
            return False 
        print("process ID to be used: " + str(procPid))
        self.procPid = procPid 
        return True 


    # Run application and login 
    def runApplication(self):
        # if application is not open 
        if not self.getProcId():
            print("Process not found, opening " + self.brand)
            self.proc = subprocess.Popen(self.path)
            time.sleep(6)
            self.procPid = self.proc.pid
        # if application is already open 
        else: 
            self.proc = psutil.Process(self.procPid) 
        # if not logged in, log in and bring it to front 
        if not self.setWindow(self.brand):
            self.setWindow(self.brand + " Sign In")
            self.activateWindow()
            self.login() 
            time.sleep(2)
            self.setWindow(self.brand)
        else:
            print("Already logged into " + self.brand)
        

    # Find and store application window information 
    def setWindow(self, windowName):
        if self.os == "nt":
            self.hwndMain = win32gui.FindWindow(None, windowName)
            if self.hwndMain:
                print("Set hwndMain to " + windowName)
                return True
            return False
            print("Failed to set hwndMain to " + windowName)
        elif self.os == "posix": 
            # ------TODO------ find window and set self.hwndMain 
            print("")


    # Bring application window to the front 
    def activateWindow(self):
        print("Bringing " + self.brand + " to front")
        if self.os == "nt":
            win32gui.ShowWindow(self.hwndMain, win32con.SW_RESTORE)
            win32gui.ShowWindow(self.hwndMain, win32con.SW_SHOWNORMAL)
            win32gui.ShowWindow(self.hwndMain, win32con.SW_SHOW)
            win32gui.SetForegroundWindow(self.hwndMain)
        elif self.os == "posix": 
            # ------TODO------ activate window for mac 
            print("")


    # Move the application window to the top left corner 
    # --Currently size is set to [318, 530]
    def moveWindow(self):
        print("Now moving " + self.brand + " to the left corner")
        if self.os == "nt": 
            if re.match("10.0.22000", platform.version()):
                win32gui.MoveWindow(self.hwndMain, 0, 0, 318, 530, True)
            elif re.match(r"10\.0\.\d*", platform.version()):
                win32gui.MoveWindow(self.hwndMain, -7, 0, 318, 530, True)
            else:
                win32gui.MoveWindow(self.hwndMain, 0, 0, 318, 530, True)
        # ------TODO------ set window size and location for mac
        elif self.os == "posix": 
            print("")


    # Log in 
    def login(self):
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


    # Function to run application, bring it to front, then move it to the corner  
    def setup(self):
        self.runApplication()
        self.activateWindow()
        self.moveWindow()


    # Log out using alt+s s shortcut 
    def logout(self):
        self.setWindow(self.brand)
        self.activateWindow()
        print("Now logging out of " + self.brand)
        self.keyboard.press(Key.alt)
        self.keyboard.press("s")
        self.keyboard.release("s")
        self.keyboard.release(Key.alt)
        self.keyboard.press("s")
        self.keyboard.release("s")


    # Exit using ctrl+q
    def close(self):
        if not self.setWindow(self.brand):
            self.setWindow(self.brand + " Sign In")
        self.activateWindow()
        print("Now closing " + self.brand)
        self.keyboard.press(Key.ctrl)
        self.keyboard.press("q")
        self.keyboard.release(Key.ctrl)
        self.keyboard.release("q")





class Installer: 

    def __init__(self, brandIndex = 0):
        self.keyboard = Controller()
        self.os = os.name
        brandTypes = ["Bria Enterprise", "Cymbus"]
        self.brand = brandTypes[brandIndex]
        if brandIndex == 0:
            self.path = '"C:\Program Files (x86)\CounterPath\Bria Enterprise\BriaEnterprise.exe"'
        elif brandIndex == 1: 
            self.path = '"C:\Program Files (x86)\Cymbus\Cymbus\cymbus.exe"'


    def clearCache(self):
        if self.os == "nt": 
            if self.brand == "Cymbus":
                CymbusTemp = os.path.expandvars(r'%APPDATA%\..\Local\Temp\Cymbus') 
                if os.path.exists(CymbusTemp):
                    shutil.rmtree(CymbusTemp)
                    print("removed " + CymbusTemp)
                CymbusRoaming = os.path.expandvars(r'%APPDATA%\Cymbus')
                if os.path.exists(CymbusRoaming):
                    shutil.rmtree(CymbusRoaming)
                    print("removed " + CymbusRoaming)
            else: 
                EnterpriseTemp = os.path.expandvars(r'%APPDATA%\..\Local\Temp\CounterPath Corporation')
                if os.path.exists(EnterpriseTemp):
                    shutil.rmtree(EnterpriseTemp)
                    print("removed " + EnterpriseTemp)
                EnterpriseRoaming = os.path.expandvars(r'%APPDATA%\CounterPath')
                if os.path.exists(EnterpriseRoaming):
                    shutil.rmtree(EnterpriseRoaming)
                    print("removed " + EnterpriseRoaming)
                EnterpriseRoaming2 = os.path.expandvars(r'%APPDATA%\CounterPath Corporation')
                if os.path.exists(EnterpriseRoaming2):
                    shutil.rmtree(EnterpriseRoaming2)
                    print("removed " + EnterpriseRoaming2)
        elif self.os == "posix": 
        # ------TODO------ delete cache for mac
            print("")
    
    def uninstall(self):
    # Search through processes and terminate it 
        print("Searching through the process to terminate...")
        pidsList = psutil.pids()
        
        if self.brand == 'Cymbus':
            client_proc_name = 'cymbus.exe'
            command = 'wmic product where name="Cymbus" call uninstall'
        else: 
            client_proc_name = 'BriaEnterprise.exe'
            command = 'wmic product where name="Bria Enterprise" call uninstall'

        for pid in pidsList:
            try:
                p = psutil.Process(pid)
                if(p.name() == client_proc_name):
                    print("Process found, terminating process ID = " + str(pid))
                    p.terminate()
            except:
                print("Bypassing Access Exception...")

        time.sleep(5)
        print("Uninstalling " + self.brand + "...")
        if self.os == "nt":
            shell.ShellExecuteEx(lpVerb='runas', lpFile='cmd.exe', lpParameters='/c '+ command)
        time.sleep(20)


    def install(self):
        print("Installing " + self.brand + "...")
        # ------TODO------ Change how we get this file path, it's hardcoded now since we don't have gui
        if self.os == "nt":
            if self.brand == "Cymbus":
                command = r"C:\Users\QA\Downloads\Builds\Cymbus_6.5.3_QA_109927.msi"
            else:
                command = r"C:\Users\QA\Downloads\Builds\Bria_Enterprise_6.5.3_QA_109929.msi"
            shell.ShellExecuteEx(lpVerb='runas', lpFile='cmd.exe', lpParameters='/c msiexec /i '+ command)
            time.sleep(20)


    def cleanInstall(self):
        self.clearCache()
        self.uninstall()


if __name__ == '__main__':
    # login = Login(0, credentials.vccs[0])
    # login.setup()
    # time.sleep(12)
    # login.logout()

    # time.sleep(10)

    # login = Login(0, credentials.ptt[1])
    # login.setup()
    # time.sleep(12)
    # login.close()
    
    
    installer = Installer(1)
    installer.uninstall()
    installer.install()