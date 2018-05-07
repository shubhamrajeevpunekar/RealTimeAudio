import wave
import scipy.io.wavfile
import os
import numpy as np

from alsa_error import noalsaerr
from channel_index import get_ip_device_index, get_op_device_index

def main():
    WAV_FILE = os.path.dirname(os.path.realpath(__file__)) + "/wavs/pyaudio_record.wav"

    wave_open = wave.open(WAV_FILE, "rb")    

    total_samples = 0
    print("wave : ndarrays ->")
    data = wave_open.readframes(4096)
    while(len(data)>0):
        wave_ndarray = np.fromstring(data, dtype = np.int16)
        print(str(wave_ndarray) + ", Samples = " + str(len(wave_ndarray)))
        total_samples += len(wave_ndarray)
        data = wave_open.readframes(4096)
    print("wave : total samples -> "  + str(total_samples))

    scipy_wav_rate, scipy_wav_ndarray = scipy.io.wavfile.read(WAV_FILE)
    print("scipy wav : ndarray ->")
    print(str(scipy_wav_ndarray) + ", Samples = " + str(len(scipy_wav_ndarray)))
  
if __name__ == '__main__':
    main()