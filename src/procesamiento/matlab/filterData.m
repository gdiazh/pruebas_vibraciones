%%%%
%%%%
function [ out ] = filterData( time, noisySignal )
	Fs = 12e3;	%12[KHz]
	[a3_6window_f, a3_6window_S] = Fourier(noisySignal, Fs);
	graficarEnTyF(time, noisySignal, a3_6window_f, a3_6window_S, ' a3_6 carrusel NOT Filtered, calib Level');

	%Filtro Pasa Banda
	% salida = bandPassFilter(noisySignal, Fs, [65 2200], [1 3500]);

	s_low = lowPassFilter(noisySignal, Fs, [2500], [3000]);
	s_filter = highPassFilter(s_low, Fs, [5], [15]);

	%Graficos en tiempo y frecuencia de salida (altura) Filtrada
	[a3_6windowFilt_f, a3_6windowFilt_S] = Fourier(s_filter, Fs);
	graficarEnTyF(time, s_filter, a3_6windowFilt_f, a3_6windowFilt_S, ' a3 carrusel Filtered, calib Level');
	out = s_filter;
end