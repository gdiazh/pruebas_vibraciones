#!/usr/bin/python

__author__ = 'gdiaz'

import numpy as np
import pandas as pd

from monitor import Monitor
from fftHandler import FFTHandler


class Time2PSD(object):
    def __init__(self, signal, time, F_max, F_min):
        self.signal = signal
        self.time = time
        self.T = self.time[-1] / len(self.time)
        self.M = len(self.time)
        self.F_min = F_min
        self.N = int(F_max / F_min)
        self.freq = np.zeros(self.N)
        self.TfSignal_mod = np.zeros(self.N)
        self.TfSignal_x = np.zeros(self.N)
        self.TfSignal_y = np.zeros(self.N)
        self.sum_tmp = []
        self.index_tmp = []

    def calcPSD(self):
        print("self.M = "+str(self.M))
        for i in range(0, self.N):
            self.freq[i] = i * self.F_min
        for i in range(0, self.N):
            x = 0
            y = 0
            for k in range(0, self.M):
                # phi = (2 * np.pi) * self.freq[i] * self.time[k]
                phi = (2 * np.pi) * self.freq[i] * (60 / 4095) * k
                x = x + (self.signal[k] * np.cos(phi))
                y = y + (self.signal[k] * np.sin(phi))
                self.sum_tmp.append(x)
            self.TfSignal_mod[i] = 60*((2 * x / self.M) ** 2 + (2 * y / self.M) ** 2)
            self.TfSignal_x[i] = x
            self.TfSignal_y[i] = y
        for j in range(0,self.N*self.M):
            self.index_tmp.append(j)

    def underSampling(self, signal, time):
        N = len(signal)
        signal_under = []
        time_under = []
        for i in range(4, N, 18):
            signal_under.append(signal[i])
            time_under.append(time[i])
        a = np.array(signal_under)
        b = np.array(time_under)
        return [a, b]

    def underSampling2(self, signal, time):
        N = len(signal)
        signal_under = []
        time_under = []
        samples_under = []

        time_window = time[0]
        accel_mean = 0
        time_mean  = 0
        window_samples = 0
        dt = time[32] - time[13]
        for i in range(5, N-1):
            print("i = "+str(i))
            if (time_window <= time[i] and time[i] < time_window + dt):#0.01035
                print("time[i] = " + str(time[i]))
                accel_mean = accel_mean + signal[i]
                time_mean = time_mean + time[i]
                window_samples = window_samples +1
            else:
                # add values mean values
                print("window_samples = " + str(window_samples))
                print("time_window = " + str(time_window))
                signal_under.append(accel_mean / (window_samples-1))
                time_under.append(time_mean / (window_samples-1))
                samples_under.append(window_samples)
                # reset values
                window_samples = 0
                accel_mean  =0
                time_mean = 0
                time_window = time[i+1]
        print("under_samples = "+str(len(signal_under)))

        a = np.array(signal_under)
        b = np.array(time_under)
        c = np.array(samples_under)
        return [a, b, c]

    def underSampling3(self, signal, time):
        N = len(signal)
        signal_under = [0]
        time_under = [0]
        j = 0
        for i in range(4, N, 18):
            if (abs(signal[i] - signal_under[j])<=0.00001 and (time[i]-time_under[j]) <= 0.02):
                print("signal[i] - signal_under[j] = "+str(signal[i] - signal_under[j]))
                print("signal_under[j] = " + str(signal_under[j]))
                pass
            else:
                signal_under.append(signal[i])
                time_under.append(time[i])
                j = j + 1
        a = np.array(signal_under)
        b = np.array(time_under)
        return [a[1:], b[1:]]

    def underSampling4(self, signal, time):
        N = len(signal)
        signal_under = []
        time_under = []
        for i in range(4, N, 18):
            out1 = 0.5253<=time[i] and time[i]<=0.5292
            out2 = 1.3740 <= time[i] and time[i] <= 1.3796
            out3 = 2.2228 <= time[i] and time[i] <= 2.2284
            out4 = 3.0724 <= time[i] and time[i] <= 3.0780
            out5 = 3.9228 <= time[i] and time[i] <= 3.9276
            out6 = 4.7724 <= time[i] and time[i] <= 4.7773
            out7 = 5.6220 <= time[i] and time[i] <= 5.6268
            out8 = 6.4707 <= time[i] and time[i] <= 6.4764
            out9 = 7.3212 <= time[i] and time[i] <= 7.3268
            out10 = 8.1853 <= time[i] and time[i] <= 8.1900
            out11 = 9.0348 <= time[i] and time[i] <= 9.0405
            out12 = 9.8844 <= time[i] and time[i] <= 9.8900
            if(out1 or out2 or out3 or out4 or out5 or out6 or out7 or out8 or out9 or out10 or out11 or out12):
                pass
            else:
                signal_under.append(signal[i])
                time_under.append(time[i])
        a = np.array(signal_under)
        b = np.array(time_under)
        return [a, b]

    def underSampling5(self, signal, time, signal_ref):
        N = len(signal)
        signal_under = []
        time_under = []
        j = 0
        for i in range(4, N, 18):
            if (abs(signal[i]-signal_ref[j]) <= 0.09):
                print("match")
                print("i, j = %d, %d" %(i, j))
                signal_under.append(signal[i])
                time_under.append(time[i])
                j = j + 1
                if (j == len(signal_ref)): break
        a = np.array(signal_under)
        b = np.array(time_under)
        return [a, b]

if __name__ == '__main__':
    # TEST
    # Input Signal:
    # Input Signal:
    signal_gen = pd.read_csv('gen_data/2019-04-04_20:00:21_randomAccel.csv')
    time_gen = signal_gen['time'].values
    accel_gen = signal_gen['accel'].values

    monitor_gen = Monitor([time_gen], [accel_gen],
                       "Random Acceleration Generated Signal", "Acceleration [g]", "Time [s]",
                       sig_name=["random accel"])
    monitor_gen.plot()

    signal = pd.read_csv('accel_data/2019-04-16_20_15_27_solobaseverticalaccel14.csv')
    time = signal['time'].values / 1000.0
    accel1x = signal['a1z'].values
    accel1y = signal['a1y'].values
    accel1z = signal['a1z'].values

    monitor1 = Monitor([time, time, time], [accel1x, accel1y, accel1z],
                       "Acceleration", "Acceleration [g]", "Time [s]",
                       sig_name=["a1x", "a1y", "a1z"])
    monitor1.plot()
    # monitor1.show()

    accel1x_window1 = accel1x[7030:10156]
    time1x_window1 = time[7030:10156]

    # accel1x_window1 = accel1x[7030:7080]
    # time1x_window1 = time[7030:7080]
    time1x_window1 = time1x_window1 - min(time1x_window1)

    monitor2 = Monitor([time1x_window1], [accel1x_window1],
                       "Acceleration Min Ampl", "Acceleration [g]", "Time [s]", marker=".",
                       sig_name=["a1x"])
    monitor2.plot()
    # monitor2.show()

    a1x_psd = Time2PSD(accel1x_window1, time1x_window1, 2000, 20)

    # calc PSD
    a1x_psd.calcPSD()

    # reference PSD
    ref_psd = pd.read_csv('gen_data/2019-04-04_20:00:21_extrapolatedExpectrum.csv')
    ref_freq = ref_psd['freq'].values
    ref_accel = ref_psd['accel'].values

    monitor3 = Monitor([a1x_psd.freq, ref_freq], [a1x_psd.TfSignal_mod, ref_accel],
                       "PSD for accelerometer signal",
                       "Acceleration [g]", "Frequency [Hz]", "log", marker=".",
                       sig_name=["PSD Generated", "PSD Specification"])
    monitor3.plot()
    monitor3.show()


