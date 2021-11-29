sys.path.append('s./env/Lib/site-packages')
import librosa

sys.path.append('.')
from frequency_analyzer import FrequencyAnalyzer
from sound_modifier import SoundModifier
from audio_recognizer import AudioRecognizer
from text_compare import TextComparer
from api_bridge import ApiBridge
from variables import *
from device_io import DeviceIO 
import time

io = DeviceIO()
io.setDevices()

time.sleep(10)



