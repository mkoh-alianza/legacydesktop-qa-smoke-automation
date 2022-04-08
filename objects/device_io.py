import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import soundfile as sf

import sys
sys.path.append('s./env/Lib/site-packages')
import librosa

class DeviceIO:
    def __init__(self):
        self.duration = 0
        self.inputData = None
        self.fs = 0
        self.inputIdx = 0
        self.outputIdx = 0
        self.backData = None
        
    def loadFile(self, filename):
        self.inputData, self.fs = librosa.load(filename)
    
    
    #Sets devices for IO manager to VB Cables
    def setDevices(self):
        info = sd.query_devices()
        for idx, x in enumerate(info):
            if x['name'] == 'CABLE-A Input (VB-Audio Cable A':
                self.inputIdx = idx
                print('foundIn')
            elif x['name'] == 'CABLE-B Output (VB-Audio Cable ':
                self.outputIdx = idx
                print('foundOut')
                
        if(self.inputIdx == 0 or self.outputIdx == 0):
            print('Unable to find the VC Cable, here are all detected audio devices:')
            print(sd.query_devices())
            print('Enter the number of the one of the VC Output')
            self.outputIdx = input()
            print('Now enter the number of one of the VC Input')
            self.inputIdx = input()
            
        sd.default.device = self.outputIdx, self.inputIdx
    
    #records for a time, based on input data size
    def record(self, filename, duration):
        self.backData = sd.rec(int(duration * self.fs), samplerate=self.fs, channels=2, dtype ='float64')
        sd.wait()
        sf.write(filename, self.backData, self.fs)
        return self.backData
    
    #plays the given audio file
    def play(self, filename):
        sd.play(self.inputData, samplerate=self.fs, channels=2, dtype='float64')
        sd.wait()
    
    def playRecord(self, filename):
        self.backData = sd.playrec(self.inputData, samplerate=self.fs, channels=2, dtype='float64')
        sd.wait()
        sf.write(filename, self.backData, self.fs)
        return self.backData