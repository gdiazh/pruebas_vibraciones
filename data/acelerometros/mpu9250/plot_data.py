import pandas
import matplotlib.pyplot as plt
import numpy as np

# Get Values
data = pandas.read_csv('2019-04-16_23_04_26_carruselhorizontal12.csv')
time = data['time'].values	#[ms]
a1x = data['a1x'].values	#[g]
a1y = data['a1y'].values	#[g]
a1z = data['a1z'].values	#[g]
a2x = data['a2x'].values	#[g]
a2y = data['a2y'].values	#[g]
a2z = data['a2z'].values	#[g]

# Show some results
N = len(a1x)		#Number of Samples
T = time[-1]/1000.0	#Total Time record [s]
n = N / T;			#Number of samples per second [S/s]
Ts = time[-1]/N;	#Estimated sampling time [s]

print("Number of Samples      		: "+str(N))
print("Total Time Record 	   [s]  : "+str(T))
print("Number of Samples 	   [S/s]: "+str(n))
print("Estimated Sampling Time [ms] : "+str(Ts))

# Plot Values
plt.figure()
plt.title('Accelerometer 1 Raw Data')
plt.ylabel('Acceleration [g]')
plt.xlabel('Time [$s$]')
plt.plot(time/1000.0, a1x)
plt.plot(time/1000.0, a1y)
plt.plot(time/1000.0, a1z)
plt.grid(which='both', axis='both')
# plt.show()

plt.figure()
plt.title('Accelerometer 2 Raw Data')
plt.ylabel('Acceleration [g]')
plt.xlabel('Time [$s$]')
plt.plot(time/1000.0, a2x)
plt.plot(time/1000.0, a2y)
plt.plot(time/1000.0, a2z)
plt.grid(which='both', axis='both')
plt.show()