import sys 
import time
import os
from os.path import exists
import subprocess   
import psutil       # pip install psutil, for closing processes 
import shutil       # for deleting cache folders
import pyautogui    # pip install opencv-python
import win32com.shell.shell as shell    # for running in admin mode
import ctypes # for running in admin mode
from PIL import Image 
from initializer import Initializer 


class Installer: 

    def __init__(self, initializer):
        self.os = os.name
        self.printProgress = initializer.printProgress
        self.installerPath = initializer.installerPath
        self.imageFolder = './../detectorImages/'
        self.scaleRatio = initializer.scaleRatio
        self.brand = initializer.brand
        


    def __imageCenterLocation__(self, filename, confidence=0.6):
        image = Image.open(self.imageFolder + filename + '.png')
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
            if (self.brand == "BriaEnterprise" and exists("C:\Program Files (x86)\CounterPath\Bria Enterprise\BriaEnterprise.exe")) or (self.brand == "Cymbus" and exists("C:\Program Files (x86)\Cymbus\Cymbus\Cymbus.exe")):
                command = f'wmic product where name="{self.brand}" call uninstall'
                shell.ShellExecuteEx(lpVerb='runas', lpFile='cmd.exe', lpParameters='/c '+ command)
                time.sleep(3)
                if self.printProgress: print("Program uninstalled")
            else:
                if self.printProgress: print("Program was not previously installed")

        elif self.os == "posix":
            print("")





    def install(self):
        self.__getFile__()
        self.__uninstall__()
        self.__clearCache__()

        if self.printProgress: print(f"Installing {self.brand}...")

        if self.os == "nt":
            time.sleep(13)
            self.proc = subprocess.Popen(['msiexec', '/i',  self.installerPath])
            if self.brand == "Cymbus":
                time.sleep(3)
                if self.__imageCenterLocation__("Install_Window") is None: 
                    print(f"Installer not found on screen")
                    raise ValueError
                self.__clickImageCenter__("Install_Agreement")
                self.__clickImageCenter__("Install_Install")
                time.sleep(7)
                self.__clickImageCenter__("Install_Finish")
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
        try: 
            initializer = Initializer()
            installer = Installer(initializer)
            # installer.install()
            installer.__closeProcess__()
        except Exception:
            input("\nPress Enter to exit...")
        except KeyboardInterrupt:
            input("\nKeyboard Interrupt detected, press Enter to exit...")

    else:
        # Re-run the program with admin rights
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
        exit(0)