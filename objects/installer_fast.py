import sys 
import time
import os
from os.path import exists
import subprocess
from tracemalloc import start   
import psutil       # pip install psutil, for closing processes 
import shutil       # for deleting cache folders
import pyautogui    # pip install opencv-python
import win32com.shell.shell as shell    # for running in admin mode
import ctypes   # for running in admin mode
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
        

    # return the location of the center of the image found on screen 
    # return none if not found 
    # raise error if filename does not exist 
    def __imageCenterLocation__(self, filename, confidence=0.6):
        try: 
            image = Image.open(self.imageFolder + filename + '.png')
            image = image.resize( [int(self.scaleRatio * s) for s in image.size] )
        except FileNotFoundError:
            if self.printProgress: print(f"[Error] Image file '{filename}' does not exist")
            raise ValueError
        loc = (pyautogui.locateCenterOnScreen(image, confidence=confidence))
        if loc is None: 
            return None 
        return loc[0], loc[1]

    
    # click the center of the given image 
    # raise value error if image not found 
    def __clickImageCenter__(self, filename, confidence=0.6):
        loc = self.__imageCenterLocation__(filename, confidence)
        if loc is None: 
            print (f"[Error] {filename} not found on screen")
            raise ValueError
        pyautogui.click(loc[0], loc[1])


    # delete cache folders 
    def __clearCache__(self):
        if self.os == "nt": 
            try: 
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
            except: 
                print("[Error] Error occured while deleting cache files, aborting\n")
                raise ValueError
        elif self.os == "posix": 
        # ---------TODO---------- delete cache for mac
            if self.printProgress: print("")

        time.sleep(5)
        if self.printProgress: print(f"Finished clearing cache for {self.brand}!\n")
    


    # Search through running processes and terminate application's process (it's forced - doesn't care if there is an ongoing call)
    def __closeProcess__(self):
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
            except psutil.AccessDenied:
                if self.printProgress: print("Bypassing Access Exception...")
            except:
                print("[Error] Error occured while terminating application process, aborting\n")
                raise ValueError

        time.sleep(5)
        if self.printProgress: print(f"Finished closing processes of {self.brand}!\n")



    def uninstall(self):
        self.__closeProcess__()
        if self.printProgress: print(f"Trying to uninstall {self.brand}...")
        if self.os == "nt":
            try: 
                if (self.brand == "BriaEnterprise" and exists("C:\Program Files (x86)\CounterPath\Bria Enterprise\BriaEnterprise.exe")) \
                or (self.brand == "Cymbus" and exists("C:\Program Files (x86)\Cymbus\Cymbus\Cymbus.exe")):
                    command = f'wmic product where name="{self.brand}" call uninstall'
                    shell.ShellExecuteEx(lpVerb='runas', lpFile='cmd.exe', lpParameters='/c '+ command)
                    time.sleep(3)
                else:
                    if self.printProgress: print("Program was not previously installed")
                    return
            except:
                print(f"[Error] Error occured while uninstalling {self.brand}, aborting\n")
                raise ValueError
        elif self.os == "posix":
            print("")

        time.sleep(5)
        if self.printProgress: print(f"Finished uninstalling {self.brand}!\n")




    def install(self):
        self.uninstall()
        self.__clearCache__()

        if self.printProgress: print(f"Installing {self.brand}...")

        if self.os == "nt":
            try: 
                self.proc = subprocess.Popen(['msiexec', '/i',  self.installerPath])
            except: 
                print(f"[Error] Error occured while installing {self.brand}, aborting\n")
                raise ValueError
            if self.brand == "Cymbus":
                time.sleep(3)
                if self.__imageCenterLocation__("Install_Window") is None: 
                    print(f"[Error] Installer not found on screen")
                    raise ValueError
                self.__clickImageCenter__("Install_Agreement")
                self.__clickImageCenter__("Install_Install")
                time.sleep(7)
                startTime = time.time()
                while time.time()-startTime < 10: 
                    if self.__imageCenterLocation__("Install_Finish") is not None:
                        self.__clickImageCenter__("Install_Finish")
                        break 
                    else: time.sleep(1) 
            else:   # Bria Enterprise doesn't require any other user input
                time.sleep(10)

        elif self.os == "posix":
            if self.printProgress: print("")

        if self.printProgress: print(f"Finished installing {self.brand}!\n")










if __name__ == '__main__':

    def is_admin():
        try: return ctypes.windll.shell32.IsUserAnAdmin()
        except: return False


    if is_admin():        
        try: 
            initializer = Initializer()     # defined under initializer.py
            installer = Installer(initializer)
            installer.install()     # Install calls __closeProcess__(), __clearCache__() and uninstall()
            input("-------------------------------\nNo issues, press enter to exit!\n")
        except ValueError:
            input("-----------------------\nPress Enter to exit...\n")
        except KeyboardInterrupt:
            input("----------------------------------------------------\nKeyboard Interrupt detected, press Enter to exit...\n")

    else:
        # Re-run the program with admin rights
        if os.name == "nt": ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
        exit(0)