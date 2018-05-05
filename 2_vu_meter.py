import pyaudio
import numpy as np
import pprint

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

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK = 1024
RECORD_SECONDS = 10

with noalsaerr():
    p=pyaudio.PyAudio()

pp = pprint.PrettyPrinter(indent=4)
for x in range(0,p.get_device_count()):
    info = p.get_device_info_by_index(x)    
    if "hw:2,0" in info["name"]:
        pp.pprint(p.get_device_info_by_index(x))
        chosen_device_index = info["index"]
        chosen_device_name = info["name"]

stream=p.open(format=FORMAT,channels=CHANNELS,rate=RATE,input=True,
              frames_per_buffer=CHUNK, input_device_index=chosen_device_index)

for i in range(int(10*RATE/CHUNK)): #go for a 10 seconds
    data = np.fromstring(stream.read(CHUNK),dtype=np.int16)
    peak=np.average(np.abs(data))*2
    bars="#"*int(50*peak/2**16)
    print("%04d %05d %s"%(i,peak,bars))

stream.stop_stream()
stream.close()
p.terminate()