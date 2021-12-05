import sys
import os

import numpy as np
import matplotlib.pyplot as plt
from scipy.io.wavfile import read, write
import scipy.signal as sps
from IPython.display import Audio
from numpy.fft import fft, ifft
import time

sys.path.append('s./env/Lib/site-packages')
import librosa

sys.path.append('./objects')
from frequency_analyzer import FrequencyAnalyzer
from sound_modifier import SoundModifier
from audio_recognizer import AudioRecognizer
from text_compare import TextComparer
from api_bridge import ApiBridge
from variables import *
from test_agent import TestAgent
from device_io import DeviceIO 
from audio_recognizer import AudioRecognizer
from constants import *
from action_clicker import ActionClicker


agent = TestAgent(WEBSOCKET_ADDRESS)


agent.io_setup()
agent.two_point_zero_one_B()

