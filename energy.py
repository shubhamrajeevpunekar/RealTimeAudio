''' calculate energy of segment '''

import sys
import scipy.io.wavfile as wavfile
import numpy as np
import os

def getEnergy(audioData):
    ''' 
    return energy of the segment
    '''

    origDtype = type(audioData[0])
    
    typeInfo = np.iinfo(origDtype)
    isUnsigned = typeInfo.min >= 0

    audioData = audioData.astype(np.int64)

    if(isUnsigned):
        signal = signal - (typeInfo.max+1)/2

    # audioEnergy = np.sum(audioData**2)/float(len(audioData))
    audioEnergy = np.linalg.norm(audioData)*10

    return audioEnergy