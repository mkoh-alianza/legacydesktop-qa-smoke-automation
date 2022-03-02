import pyautogui
# pip install opencv-python
import time 



class locationList: 
    def __init__(self):   
        self.numpad_0 = [-1, -1]
        self.numpad_1 = [-1, -1]
        self.numpad_2 = [-1, -1]
        self.numpad_3 = [-1, -1]
        self.numpad_4 = [-1, -1]
        self.numpad_5 = [-1, -1]
        self.numpad_6 = [-1, -1]
        self.numpad_7 = [-1, -1]
        self.numpad_8 = [-1, -1]
        self.numpad_9 = [-1, -1]
        self.numpad_star = [-1, -1]
        self.numpad_pound = [-1, -1]


        self.tab_dialpad = [-1, -1]
        self.tab_contacts = [-1, -1]
        self.tab_favorites = [-1, -1]
        self.tab_history = [-1, -1]
        self.tab_portal = [-1, -1]


        self.screenshare = [-1, -1] 
        self.screenshare_start = [-1, -1]
        self.screenshare_copylink = [-1, -1]
        self.screenshare_newlink = [-1, -1]


        self.conference = [-1, -1] 
        self.conference_start = [-1, -1]
        self.conference_schedule = [-1, -1]
        self.conference_copylink = [-1, -1]


        self.messages = [-1, -1] 


        self.menu_softphone = [-1, -1]
        self.softphone_account = [-1, -1]
        self.softphone_preferences = [-1, -1]
        self.softphone_signout = [-1, -1]
        self.softphone_exit = [-1, -1]


        self.menu_view = [-1, -1]
        self.view_dialpad = [-1, -1]
        self.view_contacts = [-1, -1]
        self.view_favorites = [-1, -1]
        self.view_history = [-1, -1]
        self.view_portal = [-1, -1]
        self.view_onTop = [-1, -1]
        self.view_messages = [-1, -1]
        self.view_video = [-1, -1]


        self.menu_contacts = [-1, -1]
        # TODO add contacts drop down list 
        # didn't do it because it's not used as often 


        self.menu_help = [-1, -1]
        self.help_troubleshooting = [-1, -1]
        self.help_checkUpdates = [-1, -1]
        self.help_about = [-1, -1]







class Detector:

    # brandIndex: 0 if Enterprise, 1 if Cymbus
    def __init__(self, brandIndex = 1):      
        self.button = locationList()
        brandTypes = ["Bria Enterprise", "Cymbus"]
        self.brand = brandTypes[brandIndex]
        # TODO: check for various icons and check screen zoom 
        if 1: 
            self.filelocation = './detectorImages/100_'
        else:
            self.filelocation = './detectorImages/125_'


    
    def __imageLocation__(self, filename, confidence=0.6):
        loc = (pyautogui.locateOnScreen(self.filelocation + filename + '.png', confidence=confidence))
        if loc is None:
            self.clickAppIcon()
            loc = (pyautogui.locateOnScreen(self.filelocation + filename + '.png', confidence=confidence))
        if loc is None: 
            return None 
        return loc[0], loc[1]

    def __imageCenterLocation__(self, filename, confidence=0.6):
        loc = (pyautogui.locateCenterOnScreen(self.filelocation + filename + '.png', confidence=confidence))
        if loc is None:
            self.clickAppIcon()
            loc = (pyautogui.locateCenterOnScreen(self.filelocation + filename + '.png', confidence=confidence))
        if loc is None: 
            return None 
        return loc[0], loc[1]

    def __imageSize__(self, filename, confidence=0.6):
        loc = (pyautogui.locateOnScreen(self.filelocation + filename + '.png', confidence=confidence))
        if loc is None:
            self.clickAppIcon()
            loc = (pyautogui.locateOnScreen(self.filelocation + filename + '.png', confidence=confidence))
        if loc is None: 
            return None 
        return loc[2], loc[3]
    
    def __imageLocationSize__(self, filename, confidence=0.6):
        loc = (pyautogui.locateOnScreen(self.filelocation + filename + '.png', confidence=confidence))
        if loc is None:
            self.clickAppIcon()
            loc = (pyautogui.locateOnScreen(self.filelocation + filename + '.png', confidence=confidence))
        if loc is None: 
            return None 
        return [loc[0], loc[1]], [loc[2], loc[3]]


    
    def __setNumpadLocations__(self):
        bottomLeft = self.__imageLocation__("Tab")
        tempLoc, tempSize = self.__imageLocationSize__("Call")
        topRight = [tempLoc[0] + tempSize[0], tempLoc[1] + tempSize[1] + 20]

        x_dist = topRight[0] - bottomLeft[0]
        y_dist = bottomLeft[1] - 10 - topRight[1]

        if x_dist / y_dist < 1.35:
            x_div = x_dist / 6 
            y_div = x_div * 0.55
        
        else:
            y_div = y_dist / 8
            x_div = y_div * 1.81

        center = bottomLeft[0] + (x_dist / 2)
        x_row = center - (2 * x_div)
        self.button.numpad_1[0] = x_row 
        self.button.numpad_4[0] = x_row 
        self.button.numpad_7[0] = x_row 
        self.button.numpad_star[0] = x_row 
        x_row = center - (0 * x_div)
        self.button.numpad_2[0] = x_row 
        self.button.numpad_5[0] = x_row 
        self.button.numpad_8[0] = x_row 
        self.button.numpad_0[0] = x_row 
        x_row = center + (2 * x_div)
        self.button.numpad_3[0] = x_row 
        self.button.numpad_6[0] = x_row 
        self.button.numpad_9[0] = x_row 
        self.button.numpad_pound[0] = x_row 
        
        y_row = topRight[1] + (1 * y_div)
        self.button.numpad_1[1] = y_row 
        self.button.numpad_2[1] = y_row 
        self.button.numpad_3[1] = y_row 
        y_row = topRight[1] + (3 * y_div)
        self.button.numpad_4[1] = y_row 
        self.button.numpad_5[1] = y_row 
        self.button.numpad_6[1] = y_row 
        y_row = topRight[1] + (5 * y_div)
        self.button.numpad_7[1] = y_row 
        self.button.numpad_8[1] = y_row 
        self.button.numpad_9[1] = y_row 
        y_row = topRight[1] + (7 * y_div)
        self.button.numpad_star[1] = y_row 
        self.button.numpad_0[1] = y_row 
        self.button.numpad_pound[1] = y_row 
    
    def __setMenuLocations__(self):
        location, size = self.__imageLocationSize__("Menu")
        if location is None:
            raise ValueError("Numpad not found on screen")
        y_row = location[1] + (size[1]/2)
        self.button.menu_softphone[1] = y_row
        self.button.menu_view[1] = y_row
        self.button.menu_contacts[1] = y_row
        self.button.menu_help[1] = y_row
    
        x_div = size[0] / 11.75
        self.button.menu_softphone[0] = location[0] + (x_div * 2)
        self.button.menu_view[0] = location[0] + (x_div * 5)
        self.button.menu_contacts[0] = location[0] + (x_div * 8)
        self.button.menu_help[0] = location[0] + (x_div * 11)

    def __setTabLocations__(self):
        location, size = self.__imageLocationSize__("Tab")
        if location is None:
            raise ValueError("Cymbus tabs not found on screen")
        y_row = location[1] + (size[1]/2)
        self.button.tab_dialpad[1] = y_row
        self.button.tab_contacts[1] = y_row
        self.button.tab_favorites[1] = y_row
        self.button.tab_history[1] = y_row
        self.button.tab_portal[1] = y_row
        x_div = size[0] / 10
        self.button.tab_dialpad[0] = location[0] + (x_div * 1)
        self.button.tab_contacts[0] = location[0] + (x_div * 3)
        self.button.tab_favorites[0] = location[0] + (x_div * 5)
        self.button.tab_history[0] = location[0] + (x_div * 7)
        self.button.tab_portal[0] = location[0] + (x_div * 9)
    
    def __setSoftphoneDropLocations__(self):
        # if menu_softphone location is not set, set it 
        if self.button.menu_softphone[0] == -1:
            self.__setMenuLocations__()
        # click on the softphone menu to have the dropdown list appear
        pyautogui.click(self.button.menu_softphone)
        time.sleep(2)
        location, size = self.__imageLocationSize__("SoftphoneDrop")
        if location is None:
            raise ValueError("Softphone dropdown list not found on screen")
        y_div = size[1] / 8
        self.button.softphone_account[1] = location[1] + (y_div * 1)
        self.button.softphone_preferences[1] = location[1] + (y_div * 3)
        self.button.softphone_signout[1] = location[1] + (y_div * 5)
        self.button.softphone_exit[1] = location[1] + (y_div * 7)
        x_row = location[0] + (size[0]/2)
        self.button.softphone_account[0] = x_row
        self.button.softphone_preferences[0] = x_row
        self.button.softphone_signout[0] = x_row
        self.button.softphone_exit[0] = x_row
        # click on the softphone menu again to make the dropdown list disappear
        pyautogui.click(self.button.menu_softphone)

    def __setViewDropLocations__(self):
        # if menu_view location is not set, set it 
        if self.button.menu_view[0] == -1:
            self.__setMenuLocations__()
        # click on the view menu to have the dropdown list appear
        pyautogui.click(self.button.menu_view)
        time.sleep(1.5)
        location, size = self.__imageLocationSize__("ViewDrop")
        if location is None:
            raise ValueError("View dropdown list not found on screen")
        y_div = size[1] / 16
        self.button.view_dialpad[1] = location[1] + (y_div * 1)
        self.button.view_contacts[1] = location[1] + (y_div * 3)
        self.button.view_favorites[1] = location[1] + (y_div * 5)
        self.button.view_history[1] = location[1] + (y_div * 7)
        self.button.view_portal[1] = location[1] + (y_div * 9)
        self.button.view_onTop[1] = location[1] + (y_div * 11)
        self.button.view_messages[1] = location[1] + (y_div * 13)
        self.button.view_video[1] = location[1] + (y_div * 15)
        x_row = location[0] + (size[0]/2)
        self.button.view_dialpad[0] = x_row
        self.button.view_contacts[0] = x_row
        self.button.view_favorites[0] = x_row
        self.button.view_history[0] = x_row
        self.button.view_portal[0] = x_row
        self.button.view_onTop[0] = x_row
        self.button.view_messages[0] = x_row
        self.button.view_video[0] = x_row
        # click on the softphone menu again to make the dropdown list disappear
        pyautogui.click(self.button.menu_view)
        
    def __setHelpDropLocations__(self):
        # if menu_help location is not set, set it 
        if self.button.menu_help[0] == -1:
            self.__setMenuLocations__()
        # click on the view menu to have the dropdown list appear
        pyautogui.click(self.button.menu_help)
        time.sleep(1.5)
        location, size = self.__imageLocationSize__("HelpDrop")
        if location is None:
            raise ValueError("Help dropdown list not found on screen")
        y_div = size[1] / 6
        self.button.help_troubleshooting[1] = location[1] + (y_div * 1)
        self.button.help_checkUpdates[1] = location[1] + (y_div * 3)
        self.button.help_about[1] = location[1] + (y_div * 5)
        x_row = location[0] + (size[0]/2)
        self.button.help_troubleshooting[0] = x_row
        self.button.help_checkUpdates[0] = x_row
        self.button.help_about[0] = x_row
        # click on the softphone menu again to make the dropdown list disappear
        pyautogui.click(self.button.menu_help)

    def __setTopRightIconLocations__(self):
        location, size = self.__imageLocationSize__("TopRightIcons")
        if location is None:
            raise ValueError("Cymbus icons not found on screen")
        y_row = location[1] + (size[1]/2)
        self.button.screenshare[1] = y_row
        self.button.conference[1] = y_row
        self.button.messages[1] = y_row
        x_div = size[0] / 6
        self.button.screenshare[0] = location[0] + (x_div * 1)
        self.button.conference[0] = location[0] + (x_div * 3)
        self.button.messages[0] = location[0] + (x_div * 5)

        # click on the view menu to have the dropdown list appear
        pyautogui.click(self.button.screenshare)
        time.sleep(1.5)
        location, size = self.__imageLocationSize__("ScreenshareDrop")
        if location is None:
            raise ValueError("Screenshare dropdown list not found on screen")
        y_div = size[1] / 6
        self.button.screenshare_start[1] = location[1] + (y_div * 1)
        self.button.screenshare_copylink[1] = location[1] + (y_div * 3)
        self.button.screenshare_newlink[1] = location[1] + (y_div * 5)
        x_row = location[0] + (size[0]/2)
        self.button.screenshare_start[0] = x_row
        self.button.screenshare_copylink[0] = x_row
        self.button.screenshare_newlink[0] = x_row
        # click on the softphone menu again to make the dropdown list disappear
        pyautogui.click(self.button.screenshare)

        # click on the view menu to have the dropdown list appear
        pyautogui.click(self.button.conference)
        time.sleep(1.5)
        location, size = self.__imageLocationSize__("ConferenceDrop")
        if location is None:
            raise ValueError("Conference dropdown list not found on screen")
        y_div = size[1] / 6
        self.button.conference_start[1] = location[1] + (y_div * 1)
        self.button.conference_schedule[1] = location[1] + (y_div * 3)
        self.button.conference_copylink[1] = location[1] + (y_div * 5)
        x_row = location[0] + (size[0]/2)
        self.button.conference_start[0] = x_row
        self.button.conference_schedule[0] = x_row
        self.button.conference_copylink[0] = x_row
        # click on the softphone menu again to make the dropdown list disappear
        pyautogui.click(self.button.conference)
        
        

    def clickAppIcon(self):
        if self.brand == "Cymbus":
            location = self.__imageCenterLocation__("CymbusIcon")
            pyautogui.click(location)


    def toRemote(self):
        location = self.__imageCenterLocation__("Remote")
        if location is None:
            raise ValueError("Remote icon not found on screen")
        pyautogui.click(location)


    def toLocal(self):
        location, size = self.__imageLocationSize__("RemoteConnectionBar", 0.9)
        if location is None:
            raise ValueError("Remote connection bar not found on screen")
        pyautogui.click(location[0] + (size[0] / 3), location[1] + (size[1]/2))


    def clickButton(self, buttonName):
        pyautogui.click(getattr(self.button, buttonName))


    def setButtonLocations(self):
        # self.__setTabLocations__()
        # self.__setMenuLocations__()
        # self.__setNumpadLocations__()
        # self.__setSoftphoneDropLocations__()
        # self.__setViewDropLocations__()
        # self.__setHelpDropLocations__()
        self.__setTopRightIconLocations__()

    
    def __test__(self):
        print("0\n")
        pyautogui.moveTo(self.button.numpad_0)
        # pyautogui.moveTo(self.button.numpad_0[0], self.button.numpad_0[1])
        time.sleep(1)
        print("1\n")
        pyautogui.moveTo(self.button.numpad_1)
        time.sleep(1)
        print("3\n")
        pyautogui.moveTo(self.button.numpad_3)
        time.sleep(1)
        # print("menu_softphone")
        # pyautogui.moveTo(self.button.menu_softphone)
        # time.sleep(1)
        # print("menu_help")
        # pyautogui.moveTo(self.button.menu_help)
        # time.sleep(1)
        # print("tab_dialpad")
        # pyautogui.moveTo(self.button.tab_dialpad)
        # time.sleep(1)
        # print("tab_portal")
        # pyautogui.moveTo(self.button.tab_portal)

        time.sleep(2)
        pyautogui.click(self.button.menu_softphone)
        time.sleep(1)
        print("account")
        pyautogui.moveTo(self.button.softphone_account)
        time.sleep(1)
        print("softphone_exit")
        pyautogui.moveTo(self.button.softphone_exit)
        pyautogui.click(self.button.menu_softphone)
        
        # time.sleep(2)
        # pyautogui.click(self.button.menu_view)
        # time.sleep(1)
        # print("view_dialpad")
        # pyautogui.moveTo(self.button.view_dialpad)
        # time.sleep(1)
        # print("view_video")
        # pyautogui.moveTo(self.button.view_video)
        # pyautogui.click(self.button.menu_view)
        
        time.sleep(2)
        pyautogui.click(self.button.menu_help)
        time.sleep(1)
        print("help_troubleshooting")
        pyautogui.moveTo(self.button.help_troubleshooting)
        time.sleep(1)
        print("help_about")
        pyautogui.moveTo(self.button.help_about)
        pyautogui.click(self.button.menu_help)





if __name__ == '__main__':
    time.sleep(2)
    local_detector = Detector(1) 
    local_detector.setButtonLocations()
    local_detector.clickButton("screenshare")
    time.sleep(1)
    local_detector.clickButton("screenshare_start")
    



    # local_detector = Detector(1) 
    # remote_detector = Detector(1)

    # local_detector.setButtonLocations()

    # local_detector.toRemote()
    # remote_detector.setButtonLocations()

    # time.sleep(3)
    # remote_detector.toLocal()
    # local_detector.__test__()

    # local_detector.toRemote()
    # remote_detector.__test__()






