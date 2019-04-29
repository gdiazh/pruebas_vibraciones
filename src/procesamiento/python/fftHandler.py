#!/usr/bin/python

__author__ = 'gdiaz'

import numpy as np
from monitor import Monitor

class FFTHandler(object):
    def __init__(self, signal, Fs):
        self.signal = signal
        self.Fs = Fs
        self.Ts = 1.0 / Fs
        self.N = len(signal)
        self.T = self.N / float(Fs)
        self.freq = np.arange(self.N) / self.T
        self.freq = self.freq[range(int(self.N / 2))]
        self.fft_signal = np.fft.fft(signal) / self.N  # fft computing and normalization
        self.fft_signal = self.fft_signal[range(int(self.N / 2))]

if __name__ == '__main__':
    # TEST
    time = np.linspace(0, 10, 100)
    f = 5.0 / time[-1]
    print("sin frequency: " + str(f))
    signal = np.sin(2 * np.pi * f * time)

    fft_handler = FFTHandler(signal, 10*f)

    monitor1 = Monitor([time], [signal],
                       "Test function: sin()",
                       "Amplitud", "Time [s]", marker=".")
    monitor1.plot()

    monitor2 = Monitor([fft_handler.freq], [fft_handler.fft_signal],
                       "Test function: sin()",
                       "Amplitud", "Frecuency [Hz]", marker=".")
    monitor2.plot()
    monitor2.show()