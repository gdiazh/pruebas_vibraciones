import pandas
import matplotlib.pyplot as plt
import numpy as np

signal_original = pandas.read_csv('generatedSignalTime.csv')
time = signal_original['time'].values
voltage = signal_original['signal'].values

plt.figure()
plt.title('Original Signal in time')
plt.ylabel('Accel [$G$]')
plt.xlabel('Time [$s$]')
plt.plot(time, voltage)
plt.grid(which='both', axis='both')

psd_original = pandas.read_csv('generatedSignalFreqIdeal.csv')
Fi = psd_original['FrequencyIdeal'].values
Gi = psd_original['AmplitudIdeal'].values

psd = pandas.read_csv('generatedSignalFreq.csv')
fi = psd['Frequency'].values
Gfi = psd['Amplitud'].values

plt.figure()
plt.title('PSD')
plt.ylabel('Accel [$G$]')
plt.xlabel('Time [$s$]')
# plt.yscale('log')
# plt.xscale('log')
plt.plot(fi, Gfi)
plt.plot(Fi, Gi)
plt.grid(which='both', axis='both')
plt.show()