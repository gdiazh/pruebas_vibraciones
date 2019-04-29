#!/usr/bin/python

__author__ = 'gdiaz'

import numpy as np
import pandas as pd
import time
from time import gmtime, strftime
from monitor import Monitor

class PSD2Time(object):
    def __init__(self, freqPoints, accelPoints, signalDuration):
        self.freqPoints = freqPoints            #[Hz]
        self.accelPoints = accelPoints          #[G^2/Hz]
        self.psdPoints = len(self.freqPoints)
        self.N = int(self.freqPoints[-1] / self.freqPoints[0])   # number of frequencies in the digitized spectrum
        self.T = 1.0 / self.freqPoints[0]   # frequency step in the digitized spectrum
        self.freq = np.zeros(self.N)
        self.accel = np.zeros(self.N)
        self.M = 4096                       # number of samples in the generated signal in time
        self.randomAccel = np.zeros(self.M) # generated signal in time
        self.time = np.linspace(0, signalDuration, self.M)
        # parameters for Rigol DG1022
        self.s_max = 2 ** 14 - 1  # Max level of 14-bit DAC is 16,383
        self.s_zero = 2 ** 14 / 2  # "Zero" of waveform is 8,192
        self.randomAccel_frame = np.zeros(len(self.randomAccel))
        self.trigger = np.zeros(self.M)  # reference signal in time
        self.trigger_dig = np.zeros(self.M)  # reference signal in time

    def psdSlope(self):
        # Slope of the psd frequency/acceleration power relationship is given by
        # slope = log(a2/a1) / log(f2/f1)
        m = []
        for i in range(1, self.psdPoints):
            base = np.log10(self.freqPoints[i]) - np.log10(self.freqPoints[i - 1])
            alt = np.log10(self.accelPoints[i]) - np.log10(self.accelPoints[i - 1])
            m.append(alt / base)
        return m

    def getAcceleration(self, freq):
        #The frequency f and acceleration a specified in the psd points is a power relationship of the form:
        # a = offset * f ^ (slope)
        a = 0
        m = self.psdSlope()
        offset = 0
        for i in range(1, self.psdPoints):
            if freq >= self.freqPoints[i - 1] and freq <= self.freqPoints[i]:
                offset = self.accelPoints[i - 1] / self.freqPoints[i - 1] ** m[i - 1]
                a = offset * freq ** m[i - 1]
            elif freq > max(self.freqPoints):
                offset = self.accelPoints[-1] / self.freqPoints[-1] ** m[-1]
                a = offset * freq ** m[-1]
        return a

    def calcPsdSpectrum(self):
        for i in range(0, self.N):
            self.freq[i] = float(i) / self.T
            self.accel[i] = self.getAcceleration(self.freq[i])

    def calcRandomAccel(self):
        URNi = np.random.uniform(0, 1, self.N)
        SIGi = 2 * np.pi * URNi

        for k in range(0, self.M):
            xki = 0
            for i in range(0, self.N):
                xki = xki + np.sqrt(self.accel[i]) * np.cos(2 * np.pi * self.freq[i] * self.time[k] + SIGi[i])
            self.randomAccel[k] = np.sqrt(self.T / 2.0) * xki

    def genTriggerSignal(self, filename):
        for k in range(0, self.M):
            if (self.time[k]<=2):
                self.trigger[k] = 1*np.sin(2*np.pi*0.25*self.time[k])
            elif (int(self.time[k]) % 2 == 0):
                self.trigger[k] = 1
            else:
                self.trigger[k] = 0
        # Digitize
        self.trigger_dig = np.ceil((self.s_max / 2.0) * np.array(self.trigger) + (self.s_max / 2.0))
        self.trigger_dig = self.trigger_dig.astype(np.uint16)  # Create a 16-bit integer
        self.trigger_dig.astype('int16').tofile(filename)

    def save_csv(self, x, y, x_name, y_name, file_name):
        data = {x_name: x, y_name: y}
        df = pd.DataFrame(data, columns=[x_name, y_name])
        df.to_csv(file_name)

    def digitize(self, filename):
        self.randomAccel_frame = np.ceil((self.s_max / 2.0) * np.array(self.randomAccel) + (self.s_max / 2.0))
        self.randomAccel_frame = self.randomAccel_frame.astype(np.uint16) # Create a 16-bit integer

        self.randomAccel_frame.astype('int16').tofile(filename)



if __name__ == '__main__':
    # TEST
    time_stamp = strftime("%Y-%m-%d_%H:%M:%S_", time.localtime(time.time()))
    # PSD input: NASA specifications
    freqPoints = [20, 25.6, 30, 80, 133.1, 200, 2000]            # [Hz]
    accelPoints = [0.015, 0.027, 0.08, 0.08, 0.04, 0.04, 0.002]  # [G^2/Hz]
    signalDuration = 60                         # [s]
    
    psdHandler = PSD2Time(freqPoints, accelPoints, signalDuration)

    # Extrapolated PSD
    psdHandler.calcPsdSpectrum()
    psdHandler.save_csv(psdHandler.freq, psdHandler.accel, "freq", "accel", "gen_data/"+time_stamp+"extrapolatedExpectrum.csv")
    monitor1 = Monitor([psdHandler.freq, psdHandler.freqPoints], [psdHandler.accel, psdHandler.accelPoints], "Extrapolated PSD", "Acceleration [G^2/Hz]", "Frequency [Hz]", "log", marker = "o", sig_name = ["Extrapolated", "Specification"])
    monitor1.plot()

    # Convertion to signal in time
    psdHandler.calcRandomAccel()
    psdHandler.save_csv(psdHandler.time, psdHandler.randomAccel, "time", "accel", "gen_data/"+time_stamp+"randomAccel.csv")
    monitor2 = Monitor([psdHandler.time], [psdHandler.randomAccel], "Random signal in time", "Acceleration [G]", "Time [s]", marker = ".")
    monitor2.plot()

    # Digitize and save to file
    psdHandler.digitize("gen_frame/randomVibration.rdf")
    psdHandler.save_csv(psdHandler.time, psdHandler.randomAccel_frame, "time", "accel", "gen_frame/"+time_stamp+"randomAccelFrame.csv")
    monitor3 = Monitor([psdHandler.time], [psdHandler.randomAccel_frame], "Quantized Random signal in time", "Amplitud [?]", "Time [s]", marker = ".")
    monitor3.plot()

    # Generate reference signal
    psdHandler.genTriggerSignal("gen_frame/"+time_stamp+"refSignal.rdf")
    psdHandler.save_csv(psdHandler.time, psdHandler.trigger, "time", "accel", "gen_data/"+time_stamp+"refSignal.csv")
    monitor4 = Monitor([psdHandler.time], [psdHandler.trigger], "Reference signal in time",
                       "Amplitud [?]", "Time [s]", marker=".")
    monitor4.plot()
    monitor4.show()