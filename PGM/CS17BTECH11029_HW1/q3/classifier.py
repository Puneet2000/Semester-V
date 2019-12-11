import numpy as np 
import pydub as dub
import python_speech_features as psf
import os
import scipy.io.wavfile as wav
import glob
import math
from hmm import *

def classifier(model1,model2,seq):
    if model1.likelihood(seq) > model2.likelihood(seq):
        return 1
    else:
        return 2


files = glob.glob('ba/*.wav')
data1 = []
for i in files:
    data1 += create_data(i)

files = glob.glob('be/*.wav')
data2 = []
for i in files:
    data2 += create_data(i)

data1 = np.asarray(data1)
data2 = np.asarray(data2)

model1 = HMM(100)
model1.load('ba.npy')
model2 = HMM(100)
model2.load('be.npy')

print('First data')
for i in range(len(data1)):
    seq = data1[i][0]
    print(classifier(model1,model2,seq))

print('Second data')
for i in range(len(data2)):
    seq = data2[i][0]
    print(classifier(model1,model2,seq))
