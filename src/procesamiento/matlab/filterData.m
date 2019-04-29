%%%%
%%%%
function [ salida ] = filterData( time, noisySignal )
	Fs = 12e3;	%12[KHz]
	[a3_6window_f, a3_6window_S] = Fourier(noisySignal, Fs);
	graficarEnTyF(time, noisySignal, a3_6window_f, a3_6window_S, ' a3_6 carrusel NOT Filtered, calib Level');

	%Filtro Pasa Bajos
	salida = bandPassFilter(noisySignal, Fs, [65 2200], [1 3500]);

	%Graficos en tiempo y frecuencia de salida (altura) Filtrada
	[a3_6windowFilt_f, a3_6windowFilt_S] = Fourier(salida, Fs);
	graficarEnTyF(time, salida, a3_6windowFilt_f, a3_6windowFilt_S, ' a3 carrusel Filtered, calib Level');
end