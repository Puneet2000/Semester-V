import numpy as np 
import pydub as dub
import python_speech_features as psf
import os
import scipy.io.wavfile as wav
import glob
import math

def normpdf(x, mean, sd):
    var = sd**2 + 1e-10
    return -0.5*(np.log(2*np.pi*var) + (x-mean)**2/var)

class HMM(object):

    def __init__(self, N):
        self.N = N
        self.pi = np.asarray([1./self.N for _ in range(self.N)])
        self.a = np.random.rand(self.N,self.N)
        self.a = self.a/np.sum(self.a,axis=1)
        self.mu = np.zeros(self.N)
        self.covat = np.ones(self.N)

    def log_sum_exp(self,seq):
        if abs(min(seq)) > abs(max(seq)):
            a = min(seq)
        else:
            a = max(seq)

        total = 0
        for x in seq:
            total += np.exp(x - a)
        return a + np.log(total)
        
    def forward(self, sequence):
        T = len(sequence)
        forward = np.zeros((self.N,T))
        for s in range(self.N):
            forward[s,0] = self.pi[s] + normpdf(sequence[0],self.mu[s],self.covat[s])

        for t in range(1, T):
            o = sequence[t]
            for s in range(self.N):
                sum_seq = []
                for s_ in range(self.N):
                    sum_seq.append(forward[s_,t-1] + self.a[s_][s])
                    
            forward[s,t] = self.log_sum_exp(sum_seq) + normpdf(o,self.mu[s],self.covat[s])
        return forward

    def backward(self, sequence):
        T = len(sequence)
        backward = np.zeros((self.N,T))

        for t in range(T-2,0,-1):
            o = sequence[t+1]
            for s in range(self.N):
                sum_seq = []
                for s_ in range(self.N):
                    sum_seq.append(backward[s_,t+1] + self.a[s,s_] + normpdf(o,self.mu[s_],self.covat[s_]))
            
            backward[s,t] = self.log_sum_exp(sum_seq)
        return backward

    def temp_variables(self,forward,backward,sequence):
        T = len(sequence)
        gamma = np.zeros((self.N,T))
        eta = np.zeros((self.N,self.N,T))

        for t in range(T):
            sum_ = self.log_sum_exp(forward[:,t]+ backward[:,t])
            for s in range(self.N):
                gamma[s,t] = forward[s,t] + backward[s,t] -sum_

        sum_ = np.zeros(T-1)
        for t in range(T-1):
            sum_seq = []
            for s in range(self.N):
                for s_ in range(self.N):
                   sum_seq.append(forward[s,t] + self.a[s,s_] + backward[s_,t+1] + normpdf(sequence[t+1],self.mu[s_],self.covat[s_])) 
            sum_[t] = self.log_sum_exp(sum_seq)

        for t in range(T-1):
            for s in range(self.N):
                for s_ in range(self.N):
                    eta[s,s_,t] = forward[s,t] + self.a[s,s_] + backward[s_,t+1] +  normpdf(sequence[t+1],self.mu[s_],self.covat[s_]) - sum_[t]

        return gamma,eta

    def update(self, sequence):
        forward = self.forward(sequence)
        backward = self.backward(sequence)
        gamma, eta = self.temp_variables(forward,backward,sequence)
        for s in range(self.N):
            self.pi[s] = gamma[s,0]
            for s_ in range(self.N):
                self.a[s,s_] = self.log_sum_exp(eta[s,s_,:])-self.log_sum_exp(gamma[s,:])

        for s in range(self.N):
            gamma_s = gamma[s,:]
            self.mu[s] = np.sum(np.exp(gamma_s)*sequence)/(np.sum(np.exp(gamma_s)) + 1e-10)
            self.covat[s] = np.sum(np.exp(gamma_s)*(sequence-self.mu[s])*(sequence-self.mu[s]))/(np.sum(np.exp(gamma_s)) +1e-10)

    def likelihood(self,sequence):
        forward = self.forward(sequence)
        return self.log_sum_exp(forward[:,-1])

    def save(self,path):
        np.save(path,{'pi':self.pi,'a':self.a,'mu':self.mu,'covat':self.covat})

    def load(self,path):
        param= np.load(path,allow_pickle=True).item()
        self.pi = param['pi']
        self.a = param['a']
        self.mu = param['mu']
        self.covat = param['covat']


def create_data(file_path):
    sound = dub.AudioSegment.from_file(file_path)
    data = []
    for i in range(0,len(sound),25-10):
        segment = sound[i:i+25]
        segment.export('./temp.wav',format='wav')
        (rate,sig) = wav.read("temp.wav")
        mfcc_feat = psf.mfcc(sig,rate)
        data.append(mfcc_feat)
    return data
