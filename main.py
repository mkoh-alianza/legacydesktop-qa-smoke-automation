import sys
import numpy as np
import matplotlib.pyplot as plt


from scipy.io.wavfile import read, write
import scipy.signal as sps
from IPython.display import Audio
from numpy.fft import fft, ifft

sys.path.append('s./env/Lib/site-packages')
import librosa

sys.path.append('.')
from frequency_analyzer import FrequencyAnalyzer
from sound_modifier import SoundModifier
from audio_recognizer import AudioRecognizer
from text_compare import TextComparer


print("Enter the name of the audio file to analyze")
filename = input()

output = AudioRecognizer.work(filename)

TextComparer.compareOutputToFile("word_list.txt", output)


