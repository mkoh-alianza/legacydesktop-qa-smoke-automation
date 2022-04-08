import sys 
import os
from os.path import exists
import re           # for regex
import ctypes # for running in admin mode
from tkinter import *   # pip install tk    
from tkinter.filedialog import askopenfilename
from functools import partial
from credentials import accountList



class Initializer: 

    def __init__(self):
        self.os = os.name
        self.printProgress = True
        self.installerPath = ""
        self.scaleRatio = 0
        self.brand = ""
        self.exePath = ""
        self.account = ""
        self.__setVariabes__()

        if self.brand == "":
            print("No brand selected")
            raise ValueError
            
        self.__getFile__()
        

        
    def __setVariabes__(self):

        def onButtonClick(root):
            if brandIndex.get() == 0:
                self.brand = "BriaEnterprise"
                self.exePath = '"C:\Program Files (x86)\CounterPath\Bria Enterprise\BriaEnterprise.exe"'
            elif brandIndex.get() == 1: 
                self.brand = "Cymbus"
                self.exePath = '"C:\Program Files (x86)\Cymbus\Cymbus\cymbus.exe"'

            if printBool.get() == 1:
                self.printProgress = True 
            else:
                self.printProgress = False

            self.account = account.get() 
            self.scaleRatio = int(scale.get()) / 100
            root.destroy()


        root = Tk()
        root.geometry("250x350")
        brandIndex = IntVar()
        brandIndex.set(3)
        printBool = IntVar()
        printBool.set(1)
        scale = StringVar()
        account = StringVar()
        account.set(accountList[0])

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

        Label(root, text="Select account", font=('Calibri 13')).pack( pady = (13, 5) )

        # Add more account options if needed 
        d = OptionMenu(root, account, *accountList )
        d.pack( anchor = W, padx = 10, pady = 13 )
        
        button_submit = Button(root, text ="Submit", command = partial(onButtonClick, root) )
        button_submit.pack( pady = 10 )

        label = Label(root)
        label.pack()
        root.mainloop()



    def __getFile__(self): 
        if self.os == "nt":
            initialdir='/Downloads'
            # initialdir='/'
            installerPath = askopenfilename(title="Select file to install", initialdir=initialdir)
            if self.brand == "Cymbus" and not re.match(r".*Cymbus.*", installerPath): 
                    print("File you selected does not match the brand you specified previously")
                    raise ValueError
            elif self.brand == "BriaEnterprise" and not re.match(r".*Bria_Enterprise.*", installerPath): 
                    print("File you selected does not match the brand you specified previously")
                    raise ValueError
        else: 
            print("")

        if self.os == "nt":
            installerPath = installerPath.replace("/", "\\")

        self.installerPath = installerPath





if __name__ == '__main__':

    def is_admin():
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False

    if is_admin():
        try: 
            initializer = Initializer()
        except Exception:
            input("\nPress Enter to exit...")
        except KeyboardInterrupt:
            input("\nKeyboard Interrupt detected, press Enter to exit...")

    else:
        # Re-run the program with admin rights
        if os.name == "nt": ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
        # elif self.os == "posix": os.system("""osascript -e 'do shell script "mkdir -m 0775 -p \\"%s\\" " with administrator privileges'"""%d)
        exit(0)