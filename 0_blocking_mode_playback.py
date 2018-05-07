import pyaudio
import wave
import sys
import numpy as np

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

CHUNK = 1024
DEVICE_OP_HW = "pulse"

if len(sys.argv) < 2:
    print("Plays a wave file.\n\nUsage: %s filename.wav" % sys.argv[0])
    sys.exit(-1)

wf = wave.open(sys.argv[1], 'rb')

# instantiate PyAudio 
p = pyaudio.PyAudio()

# get the output device index
for x in range(0,p.get_device_count()):
    info = p.get_device_info_by_index(x)    
    # pp.pprint(p.get_device_info_by_index(x))
    if DEVICE_OP_HW in info["name"]:
        # pp.pprint(p.get_device_info_by_index(x))
        chosen_device_index = info["index"]
        chosen_device_name = info["name"]

print("CHOSEN DEVICE : " + "index -> " + str(chosen_device_index) + ", name -> " + str(chosen_device_name))


# open stream 
stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                channels=wf.getnchannels(),
                rate = wf.getframerate(),
                # 9 : pusle, works for now but doesn't play sound
                output_device_index=9,
                output=True)

# TEST THE OUTPUT for stream
print(stream._is_output)

# read data
data = wf.readframes(CHUNK)

# play stream (3)
while len(data) > 0:
    # TODO :  Ouptut to speakers
    # just play with "aplay" from the commandline
    stream.write(data)
    
    # Output to console
    streamData = np.fromstring(data, dtype = np.int16)
    print(streamData)
    # OUTPUT CHECKED, same numpy arrays displayed while recording and playback

    data = wf.readframes(CHUNK)

# stop stream (4)
stream.stop_stream()
stream.close()

# close PyAudio (5)
p.terminate()