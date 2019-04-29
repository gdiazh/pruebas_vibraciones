%%%%
%%%%
function [ psd_filt ] = filerDPSD( noisyPSD, freqPSD )
	Fs = 12e3;	%12[KHz]
	[a2zHighPSD_f, a2zHighPSD_S] = Fourier(noisyPSD, Fs);
	graficarEnTyF(freqPSD, noisyPSD, a2zHighPSD_f, a2zHighPSD_S, ' acceleration PSD NOT Filtered, Calib Level');

	%Filtro Pasa Bajos
	psd_filt = lowPassFilter(noisyPSD, Fs, [100], [10]);

	%Graficos en tiempo y frecuencia de salida (altura) Filtrada
	[a2zHighPSDFilt_f, a2zHighPSDFilt_S] = Fourier(psd_filt, Fs);
	graficarEnTyF(freqPSD, psd_filt, a2zHighPSDFilt_f, a2zHighPSDFilt_S, ' acceleration PSD Filtered, Calib Level');

end