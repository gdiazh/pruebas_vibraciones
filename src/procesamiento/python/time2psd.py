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
    signal = pd.read_csv('gen_data/randomAccel.csv')
    time = signal['time'].values
    accel = signal['accel'].values
    time = time[8:]
    accel = accel[8:]

    signalHandler = Time2PSD(accel, time, 2000, 20)

    # calc PSD
    signalHandler.calcPSD()

    # reference PSD
    ref_psd = pd.read_csv('gen_data/extrapolatedExpectrum.csv')
    ref_freq = ref_psd['freq'].values
    ref_accel = ref_psd['accel'].values

    monitor1 = Monitor([signalHandler.freq, ref_freq], [signalHandler.TfSignal_mod, ref_accel], "Recovered PSD for generated signal",
                       "Acceleration [g]", "Frequency [Hz]", "log", marker=".", sig_name = ["PSD Generated", "PSD Specification"])
    monitor1.plot()
    # monitor1.show()
    # measured signal
    signal_m = pd.read_csv('osc_data/rw9.csv')
    time_m = signal_m['TIME'].values
    time_m = time_m + abs(time_m[0]) + 0.1205
    accel_m = signal_m['CH1'].values
    accel_m = accel_m - np.mean(accel_m)
    accel_m = accel_m * 0.3939

    signal_under = signalHandler.underSampling5(accel_m, time_m, accel)
    accel_m_under = signal_under[0]
    time_m_under = signal_under[1]
    # samples_under = signal_under[2]

    accel_m_under = accel_m_under[:-10]
    time_m_under = time_m_under[:-10]
    # samples_under = samples_under[:-10]

    monitor2 = Monitor([time, time_m, time_m_under], [accel, accel_m, accel_m_under], "Random Signal", "Acceleration [g]", "Time [s]", marker=".", sig_name = ["Generated", "Measured", "Recovered"])
    monitor2.plot()
    # monitor2.show()
    print(len(time))
    print(len(time_m))
    print(len(time_m_under))
    print("time_m_under[-1] = "+str(time_m_under[-1]))
    print("len(accel_m_under) = " + str(len(accel_m_under)))

    signalHandler_m = Time2PSD(accel_m_under, time_m_under, 2000, 20)

    # calc PSD
    signalHandler_m.calcPSD()

    monitor3 = Monitor([signalHandler_m.freq, ref_freq], [signalHandler_m.TfSignal_mod, ref_accel],
                       "Recovered PSD for measured signal",
                       "Acceleration [g^2/Hz]", "Frequency [Hz]", "log", marker=".", sig_name = ["From Generated", "From Recovered"])
    monitor3.plot()
    # monitor3.show()

    # calc FFT
    fft_handler1 = FFTHandler(accel, 2e3)
    fft_handler2 = FFTHandler(accel_m_under, 2e3)

    monitor4 = Monitor([fft_handler1.freq, fft_handler2.freq], [fft_handler1.fft_signal, fft_handler2.fft_signal],
                       "FFT",
                       "Amplitud", "Frecuency [Hz]", marker=".", sig_name = ["From Generated", "From Recovered"])
    monitor4.plot()
    # monitor4.show()
    monitor5 = Monitor([fft_handler1.freq, fft_handler2.freq], [np.abs(fft_handler1.fft_signal)**2, np.abs(fft_handler2.fft_signal)**2],
                       "FFT^2",
                       "Amplitud^2", "Frecuency [Hz]", marker=".", sig_name = ["From Generated", "From Recovered"])
    monitor5.plot()
    # monitor5.show()

    # reference signal
    ref_signal = pd.read_csv('gen_data/refSignal.csv')
    time_ref = ref_signal['time'].values
    accel_ref = ref_signal['accel'].values
    # accel_m = accel_m * 0.37

    monitor6 = Monitor([time, time_ref], [accel, accel_ref], "Generated Random and Reference Signal", "Acceleration [g]",
                       "Time [s]", sig_name = ["Generated", "Reference"])  # , marker=".")
    monitor6.plot()
    # monitor6.show()

    # Debug PSD
    monitor7 = Monitor([signalHandler.freq, signalHandler_m.freq], [signalHandler.TfSignal_x, signalHandler_m.TfSignal_x],
                       "PSD sum_x- component for measured signal",
                       "Acceleration [g]", "Frequency [Hz]", marker=".", sig_name = ["From Generated", "From Measured"])
    monitor7.plot()
    # monitor7.show()

    monitor8 = Monitor([signalHandler.index_tmp, signalHandler_m.index_tmp],
                       [signalHandler.sum_tmp, signalHandler_m.sum_tmp],
                       "PSD x- component for measured signal",
                       "Acceleration [g]", "Frequency [Hz]", marker=".", sig_name = ["From Generated", "From Recovered"])
    monitor8.plot()
    # monitor8.show()

    # Difference signal
    try:
        monitor9 = Monitor([time], [accel_m_under[0:len(time)]-accel], "Difference Signal", "Acceleration [g]", "Time [s]", marker=".", sig_name = ["Generated-Recovered Error"])
    except:
        monitor9 = Monitor([time_m_under], [accel_m_under - accel[0:len(time_m_under)]], "Difference Signal",
                       "Acceleration [g]", "Time [s]", marker=".", sig_name = ["Generated-Recovered Error"])
    monitor9.plot()
    monitor9.show()
