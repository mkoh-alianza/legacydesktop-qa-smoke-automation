import time
import requests
import csv
import zipfile
import os

class UemBridge:
    
    def __init__(self, uri, username, password):
        self.uri = uri
        self.last_res = ''
        self.session_key = ''
        self.callId = ''
        self.username = username
        self.password = password
        self.startTime = str(int(time.time() * 1000))
        self.cookies = ''
        print(self.startTime)
    '''======================================================================
                                HANDLING CONNECTIONS
    ========================================================================='''
    
    def open_connection(self):
        #self.last_res = requests.post(self.uri + "username=" + self.username + "&password=" + self.password)
        self.last_res = requests.post(self.uri + "/stretto/login?username=" + self.username + "&password=" + self.password)
        self.session_key = self.last_res.text.replace('OKsecret:', '').replace('\n', '')
        self.cookies = self.last_res.cookies
        print(self.cookies)
        print(self.session_key)
        
    def set_start_time(self, setTime=None):
    
        if(time):
            self.startTime = setTime
        else:    
            self.startTime = str(int(time.time() * 1000))
 
    def query(self, queryType, groupname, report):
        timeNow = str(int(time.time() * 1000))
        queryString = self.uri + "/stretto/download?query=" + queryType + "&groupname=" + groupname + "&X-CounterPath-CSRFP=" + str(self.session_key) + "&reportType=" + report + "&grouprollup=true" + "&start=" + self.startTime + "&end=" + timeNow
        print(queryString)
        data = requests.post(queryString, cookies=self.cookies)
        
        
        newFile = open("reports/report.zip", 'wb')
        
        newFile.write(data.content)
        
        newFile.close()
        
        with zipfile.ZipFile("reports/report.zip", 'r') as zip:
            
            zip.extractall("reports/")
            
        return zip.namelist()[0]
        
    def getNumReports(self, name):
        setfile = open("reports/" + name, 'r')
        csv_reader = csv.DictReader(setfile)
        line_count = 0
        for row in csv_reader:
            line_count += 1
        
        return line_count;