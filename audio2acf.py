#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import division
import numpy as np

def acf(x,maxlag=0,axis = -1): 
    
    from scipy.signal import fftconvolve
    
    x = np.rollaxis(x, axis)
    
    y = []
    
    for xx in x:
    
        n = xx.size
              
        if not (n & 0x1):
            xx = xx[:-1]
            n = xx.size
            
        if maxlag==0:
            maxlag = n
        
        b = np.zeros(n + maxlag)
    
        b[0:n] = xx # This works for n being even
    
        # Do an array flipped convolution, which is a correlation.
        ac = fftconvolve(b, xx[::-1], mode='valid') 
        y.append( ac/ac.max() )
        
        
    y = np.rollaxis( np.array(y), axis ) 
        
    return y
    
def wavread(file_name):
    from scipy.io.wavfile import read
    
    fs, y = read(file_name)
    return fs,np.array(y,dtype=np.float64)/(2**15-1)

def wavwrite(file_name,x,fs = 44100):
    from scipy.io.wavfile import write

    x = x/np.max(np.abs(x))*0.9
    write(file_name,fs,np.array(x*(2**15-1),dtype=np.int16))

    
if __name__ == "__main__":

    import sys
    import os
    import timeit
    import subprocess
    
    if len(sys.argv)>2:
        filename = sys.argv[1]
        maxlag = int(sys.argv[2])
    elif len(sys.argv)>1:
        filename = sys.argv[1]
        maxlag = 0
    elif len(sys.argv)>0:
        filename = "test.wav"
        maxlag = 20
        
    filename_, file_extension = os.path.splitext(filename)
    filewav = "%s" % (filename_ + r".wav")
    fileout = "%s" % ("acf_" + filename_ + ".wav")
    filemp3 = "%s" % ("acf_" + filename_ + ".mp3")
    
    if not os.path.isfile(filewav):
        
        print("Converting to WAV")               
        task = ["avconv", "-i","%s" % filename, filewav]
        subprocess.call(task)


    print("Reading WAV")
    fs,x = wavread(filewav) 
    maxlag_samples = maxlag*fs

    print("Performing ACF")
    tic=timeit.default_timer()
    y = acf(x,maxlag_samples)
    toc=timeit.default_timer()
    print("Time consumed",toc-tic)
    
    print("Normalization")

    for i in xrange(y.shape[1]):

        ntime = int(0.05*y[:,i].size)
        ramp = np.ones(y.shape[0])
        ramp[0:ntime] = (1 - np.cos(np.pi*np.arange(ntime)/ntime ) )*0.5
        y[:,i] = y[:,i]*ramp

    print("Wav writing")
    wavwrite(fileout,y,fs)

    print("Converting to Mp3")
    task = ["avconv", "-i","%s" % fileout, "-b", "320k", filemp3]
    subprocess.call(task)
    
    print("Cleaning up")
    task = ["rm",filewav]
    subprocess.call(task)

    task = ["rm",fileout]
    subprocess.call(task)
