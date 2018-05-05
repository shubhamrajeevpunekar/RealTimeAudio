import os
import pyaudio
import numpy as np
import pprint
import wave

'''
Remove the warnings from alsa when creating pyaudio.PyAudio object
-------------------------------------------------------------------
'''
from ctypes import *
from contextlib import contextmanager
ERROR_HANDLER_FUNC = CFUNCTYPE(None, c_char_p, c_int, c_char_p, c_int, c_char_p)
def py_error_handler(filename, line, function, err, fmt):
    pass

c_error_handler = ERROR_HANDLER_FUNC(py_error_handler)

@contextmanager
def noalsaerr():
    asound = cdll.LoadLibrary('libasound.so')
    asound.snd_lib_error_set_handler(c_error_handler)
    yield
    asound.snd_lib_error_set_handler(None)
'''
-------------------------------------------------------------------
'''


# TODO : make this a cmd arg
DEVICE_HW = "hw:2,0"

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK = 1024
RECORD_SECONDS = 5
OUTPUT_FILE = os.path.dirname(os.path.realpath(__file__)) + "wavs/pyaudio_record.wav"

with noalsaerr():
    p = pyaudio.PyAudio() # start the PyAudio class

# Get number of devices, iterate over each device for info, 
# and select the device matching hw signature
pp = pprint.PrettyPrinter(indent=4)
for x in range(0,p.get_device_count()):
    info = p.get_device_info_by_index(x)    
    if "hw:2,0" in info["name"]:
        pp.pprint(p.get_device_info_by_index(x))
        chosen_device_index = info["index"]
        chosen_device_name = info["name"]

print("CHOSEN DEVICE : " + "index -> " + str(chosen_device_index) + ", name -> " + str(chosen_device_name))

# open stream with this device
stream = p.open(format=FORMAT, channels=CHANNELS,rate=RATE,input_device_index=chosen_device_index, input=True,
                frames_per_buffer=CHUNK)

# write to a wav file

wavFile = wave.open("wavs/pyaudio_record.wav", "wb")
wavFile.setnchannels(1)
wavFile.setsampwidth(pyaudio.get_sample_size(pyaudio.paInt16))
wavFile.setframerate(16000)

# create a numpy array holding a single read of audio data

# we get numpy array for scipy format
# and we save a wav file using wave module
for i in range(0, int(RATE/CHUNK * RECORD_SECONDS)):
    streamData = stream.read(CHUNK)
    wavFile.writeframes(streamData)
    data = np.fromstring(streamData,dtype=np.int16)
    print(str(data) + " -> " + str(len(data)) + " samples")

# close the stream 
wavFile.close()
stream.stop_stream()
stream.close()
p.terminate()