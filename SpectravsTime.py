# -*- coding: utf-8 -*-
"""
Created on Thurs Apr 30 15:31:14 2020

@author: Apipe
"""
workdir= "\\Users\\Apipe\\OneDrive\\Desktop"
workraw="\\Users\\Apipe\\OneDrive\\Desktop"

import matplotlib.pyplot as plt
from obspy.clients.fdsn import Client
from obspy import UTCDateTime
import numpy as np
import numpy.fft as fft



#THIS CODE RETURNS THE MEDIAN NOISE POWER FOR A TRACE
def dofft(trace):
    sp=fft.fft(trace) 
#    freq=fft.fftfreq(trace.stats.npts,trace.stats.delta)
    ps = 2.0*trace.stats.delta*np.abs(sp/trace.stats.npts)**2.0
    dB = 10 * np.log10(ps)    
    median_noise= np.mean(dB)
    return median_noise


#station information
fdsn_client = Client('IRIS')
name='VGZ'
chan='HHZ'
net='CN'
location = '--'
timezone = -7
timeFix = timezone * 3600

startDate = UTCDateTime("2020-02-03T19:00:00") #7pm utc is 1pm calgary
dates = []
medianPower = []

t1 = startDate

t2 = startDate + 3600
lastDate = startDate + (84 * 86400)

while t2 <= lastDate:
    st = fdsn_client.get_waveforms(network=net, station=name, location= location,
                               channel=chan, starttime=t1, endtime=t2,attach_response=True)
    st.remove_response(output="DISP")
    medianPower.append(dofft(st[0]))
    dates.append((t2+timeFix).date) #-21600 for calgary
    t1 += 86400 
    #seconds to next day
    t2 = t2 + 86400

plt.plot(dates, medianPower)

