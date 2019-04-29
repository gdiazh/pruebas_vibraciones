close all
cd ../../../data/acelerometros/333B32PCB/
data = csvread('CarruselVertical.csv', 1, 0);
cd ../../../src/procesamiento/matlab/

a1 = data(:,2);	%43869 -> base acrilico
a2 = data(:,3);	%43875 -> soporte base
a3 = data(:,4);	%43815 -> soporte vertical
time = data(:,1);

a3window = a3(5.586e4:7.95e5);
timewindow = time(5.586e4:7.95e5);
timewindow = timewindow - min(timewindow);

figure()
plot(a1)

figure()
plot(a2)

figure()
plot(a3)

figure()
plot(time, a3)

figure()
plot(timewindow, a3window)

a3_filt = filterData( timewindow, a3window );

[pxx,w] = periodogram(a3_filt,rectwin(length(a3_filt)),length(a3_filt), 12e3, 'psd');

psd_filt = filterPSD(pxx, w);

% calcPsdSpectrum;

Grms = calcGrms(w, psd_filt, 60);

% Plot
figure()
loglog(w,pxx); hold on;grid on;
loglog(freqPoints, accelPoints, 'o-');
loglog(freq, accel, 'o-');
loglog(w(3000:end-224000),psd_filt(3000:end-224000));

title('Densidad de Potencia Espectral (PSD)')
xlabel('Frecuencia [Hz]'); ylabel('Aceleración [g^2/Hz]');
legend('Medida','Especificación','Extrapolación', 'Filtrada', 'pmpt');