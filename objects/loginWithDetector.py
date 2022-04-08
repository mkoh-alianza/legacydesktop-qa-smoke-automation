import sys 
import time
import os
from os.path import exists
import platform
import re           # for regex
import subprocess   
import psutil       # pip install psutil, for closing processes 
import shutil       # for deleting cache folders
import pyautogui    # pip install opencv-python
import win32com.shell.shell as shell    # for running in admin mode
import ctypes # for running in admin mode

from tkinter import *   # pip install tk    
from tkinter.filedialog import askopenfilename
import credentials

from PIL import Image 
from functools import partial


class locationList: 
    def __init__(self):   

        self.CymbusIcon = [-1, -1]

        # self.install_window = [-1, -1] 
        # self.install_agreement = [-1, -1] 
        # self.install_install = [-1, -1] 
        # self.install_finish = [-1, -1] 



class Login: 

    def __init__(self, brandIndex = 0, credentials = credentials.vccs[0], scale=100, printProgress = True):
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
        self.button = locationList()
        brandTypes = ["Bria Enterprise", "Cymbus"]
        self.brand = brandTypes[brandIndex]
        self.filelocation = './../detectorImages/'
        self.scaleRatio = scale / 100 


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
        if self.printProgress: print("\nSearching for the process...")
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
                    if self.printProgress: print("Process Found, Process ID = " + str(pid))
                    if(procPid != 'notFound'):
                        if self.printProgress: print(f"WARNING: Multiple instances of {client_proc_name} found! May test the incorrect one...")
                        if(proc.memory_percent() < p.memory_percent()):
                            procPid = pid
                            proc = p
                    else:
                        procPid = pid
                        proc = p
            except:
                if self.printProgress: print("Bypassing Access Exception...")

        if(procPid == 'notFound'):
            if self.printProgress: print(f"{client_proc_name} not found")
            return False 
        if self.printProgress: print("process ID to be used: " + str(procPid))
        self.procPid = procPid 
        return True 


    # Run application and login 
    def runApplication(self):
        # if application is not open 
        if not self.__getProcId__():
            if self.printProgress: print(f"Process not found, opening {self.brand}")
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
            if self.printProgress:  print(f"Already logged into {self.brand}")
        

    # Find and store application window information 
    def __setWindow__(self, windowName):
        if self.os == "nt": 
            self.hwndMain = win32gui.FindWindow(None, windowName)
            if self.hwndMain:
                if self.printProgress: print(f"Set hwndMain to {windowName}")
                return True
            return False
            if self.printProgress: print(f"Failed to set hwndMain to {windowName}")
        elif self.os == "posix": 
            # ---------TODO---------- find window and set self.hwndMain 
            print("")


    # Bring application window to the front 
    def __activateWindow__(self):
        if self.printProgress: print(f"Bringing {self.brand} to front")
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
        if self.printProgress: print(f"Now moving {self.brand} to the left corner")
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
        if self.printProgress: print("Searching through the process to terminate...")
        pidsList = psutil.pids()
        
        if self.brand == 'Cymbus':
            client_proc_name = 'cymbus.exe'
        else: 
            client_proc_name = 'BriaEnterprise.exe'

        for pid in pidsList:
            try:
                p = psutil.Process(pid)
                if(p.name() == client_proc_name):
                    if self.printProgress: print("Process found, terminating process ID = " + str(pid))
                    p.terminate()
            except:
                if self.printProgress: print("Bypassing Access Exception...")


    # Log in 
    def login(self):
        if self.printProgress: print("Loggin in...")
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
    def logout(self):
        self.__setWindow__(self.brand)
        self.__activateWindow__()
        if self.printProgress: print(f"Now logging out of {self.brand}")
        self.__mouseClick__(36, 44)
        time.sleep(1)
        self.__mouseClick__(40, 112)
        


    # Exit using mouse clicks
    def close(self):
        if not self.__setWindow__(self.brand):
            self.__setWindow__(self.brand + " Sign In")
            self.__activateWindow__()
            if self.printProgress: print(f"Now closing {self.brand}")
            location = ScreenScanner.findImage('CymbusSignIn')
            self.__mouseClick__(location[0] + 30, location[1] + 50)
        else:
            self.__activateWindow__()
            if self.printProgress: print(f"Now closing {self.brand}")
            self.__mouseClick__(36, 44)
            time.sleep(1)
            self.__mouseClick__(28, 143)






class Installer: 

    def __init__(self):
        self.os = os.name
        self.printProgress = False
        self.filepath = ""
        self.filelocation = './../detectorImages/'
        self.scaleRatio = 0
        self.brand = ""
        self.path = ""
        self.__setVariabes__()
        if self.brand == "":
            print("No brand selected")
            raise ValueError
        

        
    def __setVariabes__(self):

        def onButtonClick(root):
            if brandIndex.get() == 0:
                self.brand = "Bria Enterprise"
                self.path = '"C:\Program Files (x86)\CounterPath\Bria Enterprise\BriaEnterprise.exe"'
            elif brandIndex.get() == 1: 
                self.brand = "Cymbus"
                self.path = '"C:\Program Files (x86)\Cymbus\Cymbus\cymbus.exe"'

            if printBool.get() == 1:
                self.printProgress = True 
            else:
                self.printProgress = False

            self.scaleRatio = int(scale.get()) / 100
            root.destroy()


        root = Tk()
        root.geometry("250x270")
        brandIndex = IntVar()
        brandIndex.set(3)
        printBool = IntVar()
        printBool.set(1)
        scale = StringVar()

        Label(root, text="Select brand", font=('Calibri 13')).pack( pady = (10, 0) )

        R1 = Radiobutton(root, text="Bria Enterprise", variable=brandIndex, value=0)
        R1.pack( anchor = W, padx = 10 )

        R2 = Radiobutton(root, text="Cymbus", variable=brandIndex, value=1)
        R2.pack( anchor = W, padx = 10 )

        Label(root, text="Input screen scale", font=('Calibri 13')).pack( pady = (13, 5) )

        b = Entry(root, textvariable=scale)
        b.insert(END, '100')
        b.pack()

        c = Checkbutton(root, text = "Print progress?", variable=printBool)
        c.pack( anchor = W, padx = 10, pady = 13 )
        
        button_submit = Button(root, text ="Submit", command = partial(onButtonClick, root) )
        button_submit.pack( pady = 10 )

        label = Label(root)
        label.pack()
        root.mainloop()



    def __imageCenterLocation__(self, filename, confidence=0.6):
        image = Image.open(self.filelocation + filename + '.png')
        image = image.resize( [int(self.scaleRatio * s) for s in image.size] )
        loc = (pyautogui.locateCenterOnScreen(image, confidence=confidence))
        if loc is None: 
            return None 
        return loc[0], loc[1]

    

    def __clickImageCenter__(self, filename, confidence=0.6):
        loc = self.__imageCenterLocation__(filename, confidence)
        if loc is None: 
            print ("%s not found on screen", filename)
            raise ValueError
        pyautogui.click(loc[0], loc[1])



    def __clearCache__(self):
        if self.os == "nt": 
            if self.brand == "Cymbus":
                CymbusTemp = os.path.expandvars(r'%APPDATA%\..\Local\Temp\Cymbus') 
                if os.path.exists(CymbusTemp):
                    shutil.rmtree(CymbusTemp)
                    if self.printProgress: print(f"removed {CymbusTemp}")
                CymbusRoaming = os.path.expandvars(r'%APPDATA%\Cymbus')
                if os.path.exists(CymbusRoaming):
                    shutil.rmtree(CymbusRoaming)
                    if self.printProgress: print(f"removed {CymbusRoaming}")
            else: 
                EnterpriseTemp = os.path.expandvars(r'%APPDATA%\..\Local\Temp\CounterPath Corporation')
                if os.path.exists(EnterpriseTemp):
                    shutil.rmtree(EnterpriseTemp)
                    if self.printProgress: print(f"removed {EnterpriseTemp}")
                EnterpriseRoaming = os.path.expandvars(r'%APPDATA%\CounterPath')
                if os.path.exists(EnterpriseRoaming):
                    shutil.rmtree(EnterpriseRoaming)
                    if self.printProgress: print(f"removed {EnterpriseRoaming}")
                EnterpriseRoaming2 = os.path.expandvars(r'%APPDATA%\CounterPath Corporation')
                if os.path.exists(EnterpriseRoaming2):
                    shutil.rmtree(EnterpriseRoaming2)
                    if self.printProgress: print(f"removed {EnterpriseRoaming2}")
        elif self.os == "posix": 
        # ---------TODO---------- delete cache for mac
            if self.printProgress: print("")
    


    def __closeProcess__(self):
        # Search through processes and terminate running instances
        if self.printProgress: print("Searching through the process to terminate...")
        pidsList = psutil.pids()
        
        if self.brand == 'Cymbus':
            client_proc_name = 'cymbus.exe'
        else: 
            client_proc_name = 'BriaEnterprise.exe'

        for pid in pidsList:
            try:
                p = psutil.Process(pid)
                if(p.name() == client_proc_name):
                    if self.printProgress: print("Process found, terminating process ID = " + str(pid))
                    p.terminate()
            except:
                if self.printProgress: print("Bypassing Access Exception...")



    def __uninstall__(self):
        self.__closeProcess__()
        if self.printProgress: print(f"Trying to uninstall {self.brand}...")
        if self.os == "nt":
            if (self.brand == "Bria Enterprise" and exists("C:\Program Files (x86)\CounterPath\Bria Enterprise\BriaEnterprise.exe")) or (self.brand == "Cymbus" and exists("C:\Program Files (x86)\Cymbus\Cymbus\Cymbus.exe")):
                command = 'wmic product where name="%s" call uninstall' % self.brand
                shell.ShellExecuteEx(lpVerb='runas', lpFile='cmd.exe', lpParameters='/c '+ command)
                time.sleep(3)
                if self.printProgress: print("Program uninstalled")
            else:
                if self.printProgress: print("Program was not previously installed")

        elif self.os == "posix":
            print("")



    def __getFile__(self): 
        if self.os == "nt":
            filepath = askopenfilename(title="Select file to install", initialdir='/')
            if self.brand == "Cymbus" and not re.match(r".*Cymbus.*", filepath): 
                    print("File you selected does not match the brand you specified previously")
                    raise ValueError
            elif self.brand == "Bria Enterprise" and not re.match(r".*Bria_Enterprise.*", filepath): 
                    print("File you selected does not match the brand you specified previously")
                    raise ValueError
        else: 
            print("")

        if self.os == "nt":
            filepath = filepath.replace("/", "\\")

        self.filepath = filepath



    def install(self):
        self.__getFile__()
        self.__uninstall__()
        self.__clearCache__()

        if self.printProgress: print(f"Installing {self.brand}...")

        if self.os == "nt":
            time.sleep(13)
            # 얘도 나중에 shell=True 없애야 할지도?
            self.proc = subprocess.Popen('msiexec /i "%s"' % self.filepath, shell=True)
            if self.brand == "Cymbus":
                time.sleep(3)
                if self.__imageCenterLocation__("InstallWindow") is None: 
                    print("Installer not found on screen")
                    raise ValueError
                self.__clickImageCenter__("InstallAgreement")
                self.__clickImageCenter__("InstallInstall")
                time.sleep(7)
                self.__clickImageCenter__("InstallFinish")
            else:   # Bria Enterprise doesn't require any other user input
                time.sleep(5)

        elif self.os == "posix":
            if self.printProgress: print("")

        if self.printProgress: print(f"Finished Installing {self.brand}!")










if __name__ == '__main__':

    def is_admin():
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False

    if is_admin():
        # login = Login(1)
        # login.setup()
        # time.sleep(12)
        # login.close_mouse()

        # time.sleep(10)

        # login = Login(0, credentials.ptt[1], True)
        # login.setup()
        # time.sleep(12)
        # login.close()
        
        try: 
            installer = Installer()
            installer.install()
        except Exception:
            input("\nPress Enter to exit...")

    else:
        # Re-run the program with admin rights
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
        exit(0)