import numpy as np
import matplotlib.pyplot as plt

# Create a "fancy" function for the arbitrary waveform generator
s_max = 2**14 - 1   # Max level of 14-bit DAC is 16,383
s_zero = 2**14 / 2  # "Zero" of waveform is 8,192

# Create first half of waveform (samples 1 to 2048):  a sin function
n = np.linspace(0,4097,4098)	# Sample index for sin function
w = np.pi / 2048;      			# Normalized frequency (rad/samp)

s = np.zeros(4098)

s[0:2048] = np.ceil(s_max/2 * np.sin(w*n[0:2048]) + s_max/2);   # Sin function

# Create third quarter of waveform (samples 2049 to 3072):  "zero"
s[2048:3072] = s_zero;

# Create seventh eigth of waveform (samples 3073 to 3584):  negative full scale
s[3072:3584] = 0;

# Create eight eigth of waveform (samples 3585 to 4096):  positive half scale
s[3584:4098] = 3.0/4.0*s_max;


plt.figure()
plt.title('Waveform for Rigol DG1022 Function Generator Test')
plt.ylabel('Quantization Level')
plt.xlabel('Sample Number')
plt.plot(n, s)
plt.grid(which='both', axis='both')
plt.show()



## Save the samples to disk
s_fp = s.astype(np.uint16)                 # Create a 16-bit integer, but let's be specific.
filename = 'testFx.rdf'					   # Store in this file
s_fp.astype('int16').tofile(filename)