function [ out ] = lowPassFilter( noisySignal, Fs, WP, WS )
    %---------Filtro rechaza banda-------------------------------------------------
    fe=Fs/2;                              % Frecuencia de normalización
    Wp1=(WP)/fe;                          % Banda de paso normalizada
    Ws1=(WS)/fe;                          % Banda eliminada normalizada
    Rp1=1;                                % Atenuación de 1dB en la banda de paso
    Rs1=40;                               % Atenuación de 40 dB en la banda eliminada
    [ord1,Wn1]=buttord(Wp1,Ws1,Rp1,Rs1);  % Orden (ord) y frecuencia de corte (Wn) del filtro
    [b1,a1]=butter(ord1,Wn1,'low');       % Coef. función de transferencia del filtro
    [h1,frec1]=freqz(b1,a1,'whole',Fs);   % Respuesta en frecuencia del filtro
    figure('Name','Filtro pasa bajos','NumberTitle','off'); 
    plot(abs(h1)); title('Filtro pasa bajos'); xlabel('Frecuencia [Hz]'); ylabel('Modulo de la ganancia, |H(jw)|')
    out=filter(b1,a1,noisySignal);        % salida del filtro en tiempo
end