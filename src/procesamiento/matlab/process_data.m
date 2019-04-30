close all
cd ../../../data/acelerometros/333B32PCB/
data = csvread('CarruselVertical2.csv', 1, 0);
cd ../../../src/procesamiento/matlab/

a1 = data(:,2);	%43869 -> base acrilico
a2 = data(:,3);	%43875 -> soporte base
a3 = data(:,4);	%43815 -> soporte vertical
time = data(:,1);

a = a3;

awindow = a(5.595e4:7.967e5);
timewindow = time(5.595e4:7.967e5);
timewindow = timewindow - min(timewindow);

figure()
plot(time, a1)
grid on
title('Prueba Carrusel Vertical, Acelerómetro Carrusel')
xlabel('Tiempo [s]'); ylabel('Aceleración [g]');

figure()
plot(time, a2)
grid on
title('Prueba Carrusel Vertical, Acelerómetro Base acrilico')
xlabel('Tiempo [s]'); ylabel('Aceleración [g]');

figure()
plot(time, a3)
grid on
title('Prueba Carrusel Vertical, Acelerómetro Soporte Lateral')
xlabel('Tiempo [s]'); ylabel('Aceleración [g]');

figure()
plot(a)

figure()
plot(timewindow, awindow)

a_filt = filterData( timewindow, awindow );

[pxx,w] = periodogram(a_filt,rectwin(length(a_filt)),length(a_filt), 12e3, 'psd');

psd_filt = filterPSD(pxx, w);

% calcPsdSpectrum;

Grms = calcGrms(w(500:end-200000), psd_filt(500:end-200000), 200);

% Plot
figure()
loglog(w,pxx); hold on;grid on;
loglog(freqPoints, accelPoints, 'o-');
loglog(freq, accel, 'o-');
loglog(w(500:end-200000),psd_filt(500:end-200000));

title('PSD Prueba Carrusel Vertical Acelerómetro Soporte Lateral')
xlabel('Frecuencia [Hz]'); ylabel('Aceleración [g^2/Hz]');
legend('Medida','Especificación','Extrapolación', 'Filtrada');

% FFT Prueba Carrusel Vertical, Acelerómetro carrusel NO Filtrada