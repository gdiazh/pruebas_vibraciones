import pandas
import matplotlib.pyplot as plt
import numpy as np

signal_original = pandas.read_csv('generatedSignalTime.csv')
time_original = signal_original['time'].values
voltage_original = signal_original['signal'].values

signal = pandas.read_csv('rw7.csv')
trig = pandas.read_csv('ch2-trig7.csv')
# print(signal)

# print(signal['TIME'])
# print(type(signal['TIME']))
time = signal['TIME'].values
time = time + abs(time[0])
# time = time[0:30]
print(time[0])
print(time[10] - time[9])
# voltage = signal['CH1 Peak Detect'].values
voltage = signal['CH1'].values
voltage = voltage * 0.37
print("mean_voltage = " + str(np.mean(voltage)))
voltage = voltage - np.mean(voltage)
# voltage = voltage[0:30]

time_trig = trig['TIME'].values
time_trig = time_trig + abs(time_trig[0])

print(type(voltage))
plt.figure()
plt.title('Random vibration from osciloscope')
plt.ylabel('Volatge [V]')
plt.xlabel('Time [$s$]')
plt.plot(time_trig, trig['CH2'].values)
plt.plot(time, voltage)
plt.grid(which='both', axis='both')
# plt.show()

##########################################################################
############  under sampling   ##############################################
##########################################################################

voltage_under = []
time_under = []
aux = 0
for i in range(9, len(voltage), 18):
    voltage_under.append(voltage[i])
    aux = aux + 60.0 / 4096
    time_under.append(aux)

voltage_under = voltage_under - np.mean(voltage_under)

plt.figure()
plt.title('Under Sampling')
plt.ylabel('Volatge [V]')
plt.xlabel('Time [$s$]')
plt.plot(time_trig, trig['CH2'].values)
plt.plot(np.array(time_under), np.array(voltage_under))
plt.grid(which='both', axis='both')
# plt.show()

##########################################################################
############  time to PSD   ##############################################
##########################################################################

Fi = [20, 50, 800, 2000]  # [Hz]
Gi = [0.013, 0.08, 0.08, 0.013]  # [G^2/Hz]

Xfi2 = []
Xfi2_x = []
Xfi2_y = []
N = 100
M = len(np.array(time_under))
T = 1.0 / 20.0  # record length

print(M)

fi = []
for i in range(0, N):
    fi.append(i / T)

ti = 0
tf = 60
tk = np.linspace(ti, tf, M)

for i in range(0, N):
    x = 0
    y = 0
    # print("-----------------------------------")
    for k in range(0, M):
        x = x + (voltage_under[k] * np.cos(2 * np.pi * fi[i] * time_under[k]))
        y = y + (voltage_under[k] * np.sin(2 * np.pi * fi[i] * time_under[k]))
    Xfi2.append((2 * x / 1) ** 2 + (2 * y / 1) ** 2)
    Xfi2_x.append(x)
    Xfi2_y.append(y)

# print(Xfi2)
####################################################################################
plt.figure()
plt.title('PSD by components')
plt.ylabel('FFT Amp')
plt.xlabel('Frequency [$Hz$]')
# plt.yscale('log')
# plt.xscale('log')
# plt.plot(Fi, Gfi)
plt.plot(fi, Xfi2_y)
plt.grid(which='both', axis='both')
####################################################################################

Gfi = []
for i in range(0, N):
    Gfi.append((2 / T) * Xfi2[i])
# print(Gfi)
plt.figure()
plt.title('Recovered Power Spectral Density from Signal in time')
plt.ylabel('PSD [$G^2 / Hz$]')
plt.xlabel('Frequency [$Hz$]')
# plt.yscale('log')
# plt.xscale('log')
# plt.plot(Fi, Gfi)
plt.plot(Fi, Gi)
plt.plot(fi, Gfi)
plt.grid(which='both', axis='both')
# plt.show()

##########################################################################
############  comparison   ##############################################
##########################################################################

# dXk = voltage_original - voltage_under[0:4096]
plt.figure()
plt.title('Signal comparison in time')
plt.ylabel('Error [V]')
plt.xlabel('Time [s]')
g1, = plt.plot(np.array(time_under), np.array(voltage_under), label='under_sampled')
g2, = plt.plot(time_original, voltage_original, label='generated')
plt.grid(which='both', axis='both')
plt.legend(handles=[g1, g2])
# plt.show()
print(len(time_under))
print(len(time_original))

##########################################################################
############  FFT   ######################################################
##########################################################################

Fs = 1247;  # sampling rate
Ts = 1.0 / Fs;  # sampling interval
# t = np.arange(0,1,Ts) # time vector

n = len(voltage_under)  # length of the signal
k = np.arange(n)
T = n / Fs
frq = k / T  # two sides frequency range
frq = frq[range(int(n / 2))]  # one side frequency range

Y = np.fft.fft(voltage_under) / n  # fft computing and normalization
Y = Y[range(int(n / 2))]

fig, ax = plt.subplots(2, 1)
ax[0].plot(time_under, voltage_under)
ax[0].set_xlabel('Time')
ax[0].set_ylabel('Amplitude')
ax[1].plot(frq, abs(Y), 'r')  # plotting the spectrum
ax[1].set_xlabel('Freq (Hz)')
ax[1].set_ylabel('|Y(freq)|')
# plt.show()

Fs2 = 1247;  # sampling rate
Ts2 = 1.0 / Fs2;  # sampling interval
# t = np.arange(0,1,Ts) # time vector

n2 = len(voltage_original)  # length of the signal
k2 = np.arange(n2)
T2 = n2 / Fs2
frq2 = k2 / T2  # two sides frequency range
frq2 = frq2[range(int(n2 / 2))]  # one side frequency range

Y2 = np.fft.fft(voltage_original) / n2  # fft computing and normalization
Y2 = Y2[range(int(n2 / 2))]

fig, ax = plt.subplots(2, 1)
ax[0].plot(time_original, voltage_original)
ax[0].set_xlabel('Time')
ax[0].set_ylabel('Amplitude')
ax[1].plot(frq2, abs(Y2), 'r')  # plotting the spectrum
ax[1].set_xlabel('Freq (Hz)')
ax[1].set_ylabel('|Y(freq)|')
plt.show()
