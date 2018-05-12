import pyaudio
import numpy as np
from channel_index import get_ip_device_index

np.set_printoptions(suppress=True) # don't use scientific notation

CHUNK = 4096 # number of data points to read at a time
RATE = 44100 # time resolution of the recording device (Hz)
TARGET = 2100 # show only this one frequency
FORMAT = pyaudio.paInt16
CHANNELS = 1

p=pyaudio.PyAudio() # start the PyAudio class
stream = p.open(format=FORMAT, channels=CHANNELS,rate=RATE,input_device_index=get_ip_device_index(p, "Camera"), input=True,
                frames_per_buffer=CHUNK)


# create a numpy array holding a single read of audio data
for i in range(10): #to it a few times just to see
    data = np.fromstring(stream.read(CHUNK),dtype=np.int16)
    fft = abs(np.fft.fft(data).real)
    fft = fft[:int(len(fft)/2)] # keep only first half
    freq = np.fft.fftfreq(CHUNK,1.0/RATE)
    freq = freq[:int(len(freq)/2)] # keep only first half
    assert freq[-1]>TARGET, "ERROR: increase chunk size"
    val = fft[np.where(freq>TARGET)[0][0]]
    print(val)

# close the stream gracefully
stream.stop_stream()
stream.close()
p.terminate()