function [ f, S ] = Fourier( signal, Fs_signal )
%Calculo de transformada de fourier de una señal
n=size(signal,1);                   % Numero de datos ("muestras")
dt=1/Fs_signal;                     % Tiempo de "muestreo" [s]
fn=fft(signal);                     % Coeficientes Transformada rapida de Fourier de la señal
Fn=fftshift(fn);                    % Datos desplazados simetricamente
S=abs(Fn);                          % Magnitud de los coeficientes
df=1/(n*dt);                        % Intervalos (saltos) de frecuencia
f=-((n-1)/2)*df:df:((n-1)/2)*df;    % Vector de frecuencias [Hz]. Simetrico c/r a cero
end
