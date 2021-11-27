import pyautogui
from time import sleep
from pynput import mouse, keyboard
from pynput.mouse import Button, Controller
import os
import platform
import sys
import time

class Record:
    
    def __init__(self, source):
        self.coords = []
        self.times = [1]
        self.times.append(time.time())
        self.disable_click = False

        if platform.system() == 'Windows':
            print('\nYou can start clicking now.\nThe last click should be ending the call/conference.\n\nWhen you are finished, press the ESC key on the keyboard.\n')
        else:
            print('\nYou can start clicking now.\nThe last click should be ending the call/conference.\n\nWhen you are finished, right click to end.\n')


        if source == 'main':
            if platform.system() == 'Windows':
                """ Collect mouse on-click events until base-case """
                with mouse.Listener(on_click=self.on_click) as listener:
                    with keyboard.Listener(on_press=self.on_press) as listener:
                        listener.join()
            elif platform.system() == 'Darwin':
                with mouse.Listener(on_click=self.on_click) as listener:
                    listener.join()
        else:
            mouse_listener = mouse.Listener(on_click=self.on_click)
            mouse_listener.start()
            
            if platform.system() == 'Windows':
                keyboard_listener = keyboard.Listener(on_press=self.on_press)
                keyboard_listener.start()
        

    """ On click listener """
    def on_click(self, x, y, button, pressed):
        if pressed and not self.disable_click:
            print('Adding click coordinates.')
            if button == Button.right:
                l_r = 'right'
            else:
                l_r = 'left'
            if platform.system() == 'Darwin' and l_r == 'right':
                print('Stopping recording.')
                print('\nUser finished clicking, saving sequence.\n')
                self.disable_click = True
                return False
            self.coords.append((x, y, time.time() - self.times[0], l_r))
            self.times[0] = time.time()


    """ On key press listener """
    def on_press(self, key):
        if key == keyboard.Key.esc:
            print('Stopping recording.')
            print('\nUser finished clicking, saving sequence.\n')

            # Used by recording from gui only
            self.disable_click = True
            return False          


    """ Get coords list """
    def get_coords(self):
        return self.coords

 
if __name__ == '__main__':
    if getattr(sys, 'frozen', False) and platform.system() == 'Darwin':
        os.chdir(os.path.dirname(sys.executable))

    print("Enter a name for this action:")
    filename = input()

    record = Record('main')
    
    print(record.coords)
    with open(os.getcwd() + '/actions/' + filename + '.txt', 'w') as f:
        for coord in record.coords:
            f.write(str(coord) + '\n')

