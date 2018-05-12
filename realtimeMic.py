import os
import pyaudio
import numpy as np
import pprint
import wave

from alsa_error import noalsaerr
from channel_index import get_ip_device_index
from energy import getEnergy

def getThreshold(stream, RATE, CHUNK, BASELINE_SECONDS):
    maxChunks = []
    for i in range(0,int(RATE/CHUNK*BASELINE_SECONDS)):
        streamData = stream.read(CHUNK)
        streamData = np.fromstring(streamData, np.int16)
        maxChunks.append(np.max(streamData))
    maxChunks = np.array(maxChunks)
    # print(maxChunks)
    THRESHOLD = np.mean(maxChunks)
    return THRESHOLD

def isSilent(audioChunk, THRESHOLD):
    "Returns 'True' if below the 'silent' threshold"
    print("MAX : " + str(np.max(audioChunk)))
    return np.max(audioChunk) < THRESHOLD

def main():

    # setup 
    DEVICE_IP_HW = "Camera" # this usually is hw:2,0
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000
    CHUNK = 4096
    BASELINE_SECONDS = 2
    RECORD_SECONDS = 5
    OUTPUT_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), "realtimeMicRecordings")

    with noalsaerr():
        p = pyaudio.PyAudio() # start the PyAudio class

    # open stream with this device
    stream = p.open(format=FORMAT, channels=CHANNELS,rate=RATE,input_device_index=get_ip_device_index(p, DEVICE_IP_HW), input=True,
                    frames_per_buffer=CHUNK)

    

    THRESHOLD = getThreshold(stream, RATE, CHUNK, BASELINE_SECONDS) - 2000
    print("THRESHOLD : " + str(THRESHOLD))

    utterance = 0
    while(True):

        audioData = b'' # binary string to hold 5 second utterances
        
        # set up a wav container for each utterance 
        wavFile = wave.open(os.path.join(OUTPUT_DIR, "mic_" + str(utterance) + ".wav"), "w")
        wavFile.setnchannels(1)
        wavFile.setsampwidth(pyaudio.get_sample_size(pyaudio.paInt16))
        wavFile.setframerate(16000)
        for i in range(0, int(RATE/CHUNK * RECORD_SECONDS)):
            streamData = stream.read(CHUNK)
            audioData += streamData       
      
        wavFile.writeframes(audioData)
        wavFile.close()
        print("saved " + os.path.join(OUTPUT_DIR, "mic_" + str(utterance) + ".wav"))
        utterance += 1


    # close the stream 
    wavFile.close()
    stream.stop_stream()
    stream.close()
    p.terminate()



if __name__ == '__main__':
    main()