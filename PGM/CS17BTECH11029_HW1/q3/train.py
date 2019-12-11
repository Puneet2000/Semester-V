import numpy as np 
import pydub as dub
import python_speech_features as psf
import os
import scipy.io.wavfile as wav
import glob
import math
from hmm import *

files = glob.glob('be/*.wav')
data = []
for i in files:
    data += create_data(i)

data = np.asarray(data)

model = HMM(100)

for i in range(len(data)):
    seq = data[i][0]
    model.update(seq)
    model.save('be.npy')
    print(model.likelihood(seq))