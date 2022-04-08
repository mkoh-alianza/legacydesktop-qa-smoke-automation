import sys 
import time
import os
from os.path import exists
import psutil       # pip install psutil, for detecting processes 
import pyautogui    # pip install opencv-python
pyautogui.useImageNotFoundException()
from PIL import Image 
from initializer import Initializer


class Click_Installer: 

    def __init__(self, initializer):
        self.os = os.name
        self.printProgress = initializer.printProgress
        self.installerPath = initializer.installerPath
        self.imageFolder = './../detectorImages/'
        self.scaleRatio = initializer.scaleRatio
        self.brand = initializer.brand
        
        # self.printProgress = True
        # self.installerPath = "C:/Users/QA/Downloads/Bria_Enterprise_6.5.4_QA4_110355.msi"
        # # self.installerPath = "C:/Users/QA/Downloads/Cymbus_6.5.4_QA4_110352.msi"
        # self.imageFolder = './../detectorImages/'
        # self.scaleRatio = 1
        # self.brand = "BriaEnterprise"
        # # self.brand = "Cymbus"


    
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


    def __deleteFolder__(self, path):
        if exists(path):
            if self.os == "nt": 
                pyautogui.press("esc")
                time.sleep(1)
                pyautogui.press("win")
                pyautogui.write("run")
                pyautogui.press("enter")
                time.sleep(0.5)
                pyautogui.write(path)
                pyautogui.press("enter")
                time.sleep(0.5)
                pyautogui.press("backspace")
                pyautogui.press("delete")
                time.sleep(0.5)
                if self.__imageLocation__("FolderInUse"):
                    self.__clickImageCenter__("FolderInUse_Cancel")
                    if self.printProgress: print(f"{path} folder in use, could not delete\n")
                else: 
                    if self.printProgress: print(f"{path} folder deleted\n")
                pyautogui.hotkey("alt", "f4")
            if self.os == "posix":
                print("I don't know yet")
        else: 
            if self.printProgress: print(f"{path} folder not found, no action required\n")


    def clearCache(self):
        # 이거 미팅 끝나고 복구 시키기!!!!! 
        # self.closeApplication()
        time.sleep(2)
        if self.os == "nt": 
            if self.brand == "Cymbus":
                self.__deleteFolder__(os.path.join(os.environ['APPDATA'], '..\Local\Temp\Cymbus'))
                self.__deleteFolder__(os.path.join(os.environ['APPDATA'], 'Cymbus'))
            else:
                self.__deleteFolder__(os.path.join(os.environ['APPDATA'], '..\Local\Temp\CounterPath Corporation'))
                self.__deleteFolder__(os.path.join(os.environ['APPDATA'], 'CounterPath'))
                self.__deleteFolder__(os.path.join(os.environ['APPDATA'], 'CounterPath Corporation'))
        elif self.os == "posix": 
        # ---------TODO---------- delete cache for mac
            if self.printProgress: print("")
    

    def closeApplication(self):
        if self.__clickImageCenter__(f"{self.brand}Icon", "right"): 
            time.sleep(1) 
            if self.__clickImageCenter__("Icon_Exit"): 
                if self.__imageLocation__("ConfirmExit"): 
                    self.__clickImageCenter__("ConfirmExit_Yes")
            else: 
                self.__clickImageCenter__("Icon_Close")
        pyautogui.press("esc")   
        if self.__clickImageCenter__(f"{self.brand}Icon_corner", "right", 0.8): 
            time.sleep(1)
            self.__clickImageCenter__("Icon_Corner_Exit")
        else: 
            if self.printProgress: print("Application not running\n")
            

    # 안쓰이면 삭제하셈 
    def __checkProcess__(self):
        # Search through processes and see if application is running
        if self.printProgress: print(f"Determining if {self.brand} is running...\n")
        pidsList = psutil.pids()
        
        if self.brand == 'Cymbus':
            client_proc_name = 'cymbus.exe'
        else: 
            client_proc_name = 'BriaEnterprise.exe'

        for pid in pidsList:
            try:
                p = psutil.Process(pid)
                if(p.name() == client_proc_name):
                    if self.printProgress: print("Application process found\n")
                    return True 
            except:
                continue 



    def uninstall(self):
        self.closeApplication()
        time.sleep(5)
        if self.printProgress: print(f"Trying to uninstall {self.brand}...")
        if self.os == "nt":
            if (self.brand == "BriaEnterprise" and exists("C:\Program Files (x86)\CounterPath\Bria Enterprise\BriaEnterprise.exe")) \
            or (self.brand == "Cymbus" and exists("C:\Program Files (x86)\Cymbus\Cymbus\Cymbus.exe")):
                pyautogui.press("esc")
                time.sleep(1)
                pyautogui.press("win")
                time.sleep(0.5)
                if self.brand == "Cymbus": 
                    pyautogui.write("uninstall cymbus")
                else: 
                    pyautogui.write("uninstall bria enterprise")
                pyautogui.press("enter")
                time.sleep(0.5)
                pyautogui.press("enter")
                time.sleep(2)

                if self.__imageLocation__("Uninstall_ProcessOpen"): 
                    self.__clickImageCenter__("Uninstall_Ok")
                    tempPrintProgress = self.printProgress  # temporarily pause printing because of the loop 
                    self.printProgress = False
                    time.sleep(5)
                    startTime = time.time() 
                    while (time.time() - startTime < 60) : 
                        if self.__imageLocation__("Uninstall_ProcessOpen"): 
                            self.__clickImageCenter__("Uninstall_Ok")
                        if self.__imageLocation__("Uninstall_CloseUnable"):
                            self.__clickImageCenter__("Uninstall_Ok")
                        if self.__imageLocation__("Uninstall_Restart"):
                            self.__clickImageCenter__("Uninstall_No")
                            break 
                    self.printProgress = tempPrintProgress 
                else: 
                    time.sleep(10)
                if self.printProgress: print(f"Uninstalled {self.brand}\n")
            elif self.printProgress: print(f"{self.brand} not installed\n")
        elif self.os == "posix":
            print("")


    def install(self): 
        if self.printProgress: print(f"Trying to install {self.brand}...")
        if self.os == "nt":
            pyautogui.press("esc")
            time.sleep(1)
            pyautogui.press("win")
            pyautogui.write("run")
            pyautogui.press("enter")
            time.sleep(0.5)
            pyautogui.write(self.installerPath)
            pyautogui.press("enter")
            if self.brand == "Cymbus":
                time.sleep(5)
                if not self.__imageLocation__("Install_Window"): 
                    print("Installer not found on screen")
                    raise ValueError
                self.__clickImageCenter__("Install_Agreement", 'left', 0.9)
                self.__clickImageCenter__("Install_Install", 'left', 0.9)
                time.sleep(15)
                self.__clickImageCenter__("Install_Finish", 'left', 0.9)
            else: time.sleep(10)
        elif self.os == "posix":
            print("")





if __name__ == '__main__':
    
    try: 
        initializer = Initializer()
        click_installer = Click_Installer(initializer)

        # click_installer.uninstall()
        # click_installer.clearCache()
        # click_installer.install()
        input("\nNo issues, press enter to exit!")
    except Exception:
        input("\nPress Enter to exit...")
    except KeyboardInterrupt:
        input("\nKeyboard Interrupt detected, press Enter to exit...")

    