close all
%% Psd Specification
freqPoints = [20, 25.6, 30, 80, 133.1, 200, 2000];            % [Hz]
accelPoints = [0.015, 0.027, 0.08, 0.08, 0.04, 0.04, 0.002];  % [G^2/Hz]


%% Calc psd slope
% Slope of the psd frequency/acceleration power relationship is given by
% slope = log(a2/a1) / log(f2/f1)
m = [];
psdPoints =  length(freqPoints);

for i = 2:psdPoints
    base = log10(freqPoints(i)) - log10(freqPoints(i - 1));
    alt = log10(accelPoints(i)) - log10(accelPoints(i - 1));
    m(i-1) = (alt / base);
end

%% Calc Spectrum
N = int16(freqPoints(end) / freqPoints(1));   % number of frequencies in the digitized spectrum
T = 1.0 / freqPoints(1);   % frequency step in the digitized spectrum
freq = [];
accel = [];
for j = 1:N
	freq(j) = (j -1)/ T;
	% Calc Acceleration
	% The frequency f and acceleration a specified in the psd points is a power relationship of the form:
	% a = offset * f ^ (slope)
	a = 0;
	for i = 2:psdPoints
	    if freq(j) >= freqPoints(i - 1) && freq(j) <= freqPoints(i)
	        offset = accelPoints(i - 1) / (freqPoints(i - 1) ^ m(i - 1));
	        a = offset * ( freq(j) ^ m(i - 1) );
	    elseif freq(j) > max(freqPoints)
	        offset = accelPoints(end) / ( freqPoints(end) ^ m(end) );
	        a = offset * ( freq(j) ^ m(end) );
	     end
	end
	accel(j) = a;

end

% Plot

loglog(freqPoints, accelPoints, 'o-');
title('Densidad de Potencia Espectral (PSD)')
xlabel('Frecuencia [Hz]'); ylabel('Aceleración [g^2/Hz]');
hold on;
grid on;
loglog(freq, accel, 'o-');
legend('Especificación','Extrapolación');