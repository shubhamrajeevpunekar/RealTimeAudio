import pyaudio
import numpy as np
import math
import audioop

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


def audio_ints(stream, num_samples=20, CHUNK=4096):
    """ Gets average audio intensity of your mic sound. You can use it to get
        average intensities while you're talking and/or silent. The average
        is the avg of the 20% largest intensities recorded.
    """
    values = [math.sqrt(abs(audioop.avg(stream.read(CHUNK), 4)))
              for x in range(num_samples)]
    values = sorted(values, reverse=True)
    # r = sum(values[:int(num_samples * 0.2)]) / int(num_samples * 0.2)
    r = sum(values) / int(num_samples)
    return r

def main():        
    # TODO : make this a cmd arg
    DEVICE_IP_HW = "Camera" # this usually is hw:2,0
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000
    CHUNK = 4096

    with noalsaerr():
        p = pyaudio.PyAudio() # start the PyAudio class

    # Get number of devices, iterate over each device for info, 
    # and select the device matching hw signature
    # pp = pprint.PrettyPrinter(indent=4)
    for x in range(0,p.get_device_count()):
        info = p.get_device_info_by_index(x)    
        # pp.pprint(p.get_device_info_by_index(x))
        if DEVICE_IP_HW in info["name"]:
            # pp.pprint(p.get_device_info_by_index(x))
            chosen_device_index = info["index"]
            chosen_device_name = info["name"]

    print("CHOSEN DEVICE : " + "index -> " + str(chosen_device_index) + ", name -> " + str(chosen_device_name))

    # open stream with this device
    stream = p.open(format=FORMAT, channels=CHANNELS,rate=RATE,input_device_index=chosen_device_index, input=True,
                    frames_per_buffer=CHUNK)

    print(" Average audio intensity for silence : " + str(audio_ints(stream)))

    stream.close()
    p.terminate()

if (__name__ == '__main__'):
    main()


    


    
    
