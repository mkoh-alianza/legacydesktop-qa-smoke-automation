import sys
import numpy as np
import matplotlib.pyplot as plt


from scipy.io.wavfile import read, write
import scipy.signal as sps
from IPython.display import Audio
from numpy.fft import fft, ifft

sys.path.append('./env/Lib/site-packages')
import librosa

sys.path.append('.')

from sound_modifier import SoundModifier



data, Fs = librosa.load('test.wav', sr=16000)
data2, Fs2 = librosa.load('test5.wav', sr=16000)

print(Fs)
print(Fs2)

dataL = (data).tolist()

dataL2 = (data2).tolist()

plt.figure()
plt.plot(dataL)
plt.xlabel('Sample Index')
plt.ylabel('Amplitude')
plt.title('Waveform of Test Audio')
plt.show()

plt.figure()
plt.plot(dataL2)
plt.xlabel('Sample Index')
plt.ylabel('Amplitude')
plt.title('Waveform of Test Audio')
plt.show()

sound = SoundModifier(dataL, dataL2, 7)

newData = sound.pinPoint()

plt.figure()
plt.plot(newData)
plt.xlabel('Sample Index')
plt.ylabel('Amplitude')
plt.title('Waveform of Test Audio')
plt.show()

print(sound.cosineSimilarity())

x = input()