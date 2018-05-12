import pyaudio
import numpy as np
import pylab
import time

DEVICE_IP_HW = "Camera" # this usually is hw:2,0
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK = 4096
RECORD_SECONDS = 10


def soundplot(stream):
    t1 = time.time() # Returns current time in seconds since epoch
    data = np.fromstring(stream.read(CHUNK), dtype=np.int16)
    pylab.plot(data)
    # pylab.title(i)
    pylab.grid()
    pylab.axis([0,len(data),-2**16/2, 2**16/2])
    pylab.savefig("03.png", dpi=100)
    pylab.close("all")
    print("took %.02f ms"%((time.time() - t1)*1000))

def main():
    p = pyaudio.PyAudio()

    for x in range(0,p.get_device_count()):
        info = p.get_device_info_by_index(x)    
        if DEVICE_IP_HW in info["name"]:
            chosen_device_index = info["index"]
            chosen_device_name = info["name"]

    print("CHOSEN DEVICE : " + "index -> " + str(chosen_device_index) + ", name -> " + str(chosen_device_name))

    stream = p.open(format=FORMAT, channels=CHANNELS,rate=RATE,input_device_index=chosen_device_index, input=True,
                frames_per_buffer=CHUNK)

    # for i in range(int(RECORD_SECONDS*RATE/CHUNK)) : # for 10 seconds
    #     soundplot(stream)
    
    while True:
        soundplot(stream)
        
    stream.stop_stream()
    stream.close()
    p.terminate()


if __name__ == '__main__':
    main()