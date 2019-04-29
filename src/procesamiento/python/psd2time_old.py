import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# PSD input: NASA
Fi = [20, 50, 800, 2000]  # [Hz]
Gi = [0.013, 0.08, 0.08, 0.013]  # [G^2/Hz]

# PSD Convertion to Time Domain
T = 1.0 / Fi[0]  # record length
# T = 1.0/10
# N = len(Fi)		#number of frequencies in the digitized spectrum
N = Fi[-1] / Fi[0]  # number of frequencies in the digitized spectrum
# N = 200

# Slope of the curve
m = []
for i in range(1, len(Fi)):
    base = np.log10(Fi[i]) - np.log10(Fi[i - 1])
    alt = np.log10(Gi[i]) - np.log10(Gi[i - 1])
    m.append(alt / base)


def G_f(f):
    Gn = 0
    for i in range(1, len(Fi)):
        if f >= Fi[i - 1] and f <= Fi[i]:
            Const = Gi[i - 1] / Fi[i - 1] ** m[i - 1]
            Gn = Const * f ** m[i - 1]
        elif f > max(Fi):
            Const = Gi[-1] / Fi[-1] ** m[-1]
            Gn = Const * f ** m[-1]
    return Gn


FFi = []
GGi = []

for i in range(0, int(N)):
    FFi.append(i / T)
    GGi.append(G_f(i / T))

plt.figure()
plt.title('Recovered Power Spectral Density from Signal in time')
plt.ylabel('PSD [$G^2 / Hz$]')
plt.xlabel('Frequency [$Hz$]')
plt.yscale('log')
plt.xscale('log')
plt.plot(FFi, GGi)
plt.grid(which='both', axis='both')
# plt.show()

fi = []
for i in range(0, int(N)):
    fi.append(i / T)
# print("fi = "+str(fi))
# print(len(fi))

URNi = np.random.uniform(0, 1, int(N))
SIGi = 2 * np.pi * URNi

M = 4096
Xk = []
ti = 0
tf = 60
tk = np.linspace(ti, tf, M)

for k in range(0, M):
    xki = 0
    for i in range(0, int(N)):
        # xki = xki + np.sqrt(Gi[i])*np.cos(2*np.pi*fi[i]*tk[k]+SIGi[i])
        xki = xki + np.sqrt(G_f(fi[i])) * np.cos(2 * np.pi * fi[i] * tk[k] + SIGi[i])
    # xki = xki + np.sqrt(G_f(i/T))*np.cos(2*np.pi*fi[i]*tk[k]+SIGi[i])
    Xk.append(np.sqrt(T / 2) * xki)

# print("Xk = "+str(Xk))
# print(len(tk))
print(len(Xk))

plt.figure()
plt.title('Input Signal in time')
plt.ylabel('Accel [$g$]')
plt.xlabel('Time [$s$]')
plt.plot(tk, Xk)
plt.grid(which='both', axis='both')
# plt.show()

# save signal to csv file
raw_data = {'time': tk,
            'signal': Xk}
df0 = pd.DataFrame(raw_data, columns=['time', 'signal'])
df0.to_csv('generatedSignalTime.csv')

# Create the waveform for rigol DG1022
s_max = 2 ** 14 - 1  # Max level of 14-bit DAC is 16,383
s_zero = 2 ** 14 / 2  # "Zero" of waveform is 8,192

Xk_rigol = np.ceil((s_max / 2) * np.array(Xk) + (s_max / 2) * np.ones(len(Xk)))

## Save the samples to disk
Xk_rigol_fp = Xk_rigol.astype(np.uint16)  # Create a 16-bit integer, but let's be specific.
filename = 'randomVibration.rdf'  # Store in this file
# Xk_rigol_fp.astype('int16').tofile(filename)

plt.figure()
plt.title('Quantized Input Signal in time')
plt.ylabel('Quantization Level')
plt.xlabel('Sample Number')
plt.plot(Xk_rigol)
plt.grid(which='both', axis='both')
# plt.show()

##########################################################################
############  time to PSD   ##############################################
##########################################################################

Xfi2 = []
Xfi2_x = []
Xfi2_y = []

for i in range(0, int(N)):
    x = 0
    y = 0
    # print("-----------------------------------")
    for k in range(0, M):
        x = x + (Xk[k] * np.cos(2 * np.pi * fi[i] * tk[k]))
        y = y + (Xk[k] * np.sin(2 * np.pi * fi[i] * tk[k]))
    # if k==25:
    # 	print("tk[k] = "+str(tk[k]))
    # 	print("Fi[i] = "+str(fi[i]))
    # 	print(x+y)
    # 	print(x)
    # 	print(y)
    Xfi2.append((2 * x / M) ** 2 + (2 * y / M) ** 2)
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
for i in range(0, int(N)):
    Gfi.append((2 / T) * Xfi2[i])
# print(Gfi)

# save signal to csv file
raw_freq_data = {'FrequencyIdeal': Fi,
                 'AmplitudIdeal': Gi
                 }
df1 = pd.DataFrame(raw_freq_data, columns=['FrequencyIdeal', 'AmplitudIdeal'])
# df1.to_csv('generatedSignalFreqIdeal.csv')

raw_freq_data2 = {'Frequency': fi,
                  'Amplitud'	: Gfi
        		 }
df2 = pd.DataFrame(raw_freq_data2, columns = ['Frequency', 'Amplitud'])
# df2.to_csv('generatedSignalFreq.csv')

plt.figure()
plt.title('Recovered Power Spectral Density from Signal in time')
plt.ylabel('PSD [$G^2 / Hz$]')
plt.xlabel('Frequency [$Hz$]')
plt.yscale('log')
plt.xscale('log')
# plt.plot(Fi, Gfi)
plt.plot(Fi, Gi)
plt.plot(fi, Gfi)
plt.grid(which='both', axis='both')
plt.show()
