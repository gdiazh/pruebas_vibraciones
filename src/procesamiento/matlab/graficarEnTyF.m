function [ ] = graficarEnTyF( t_vector, t_signal, f_vector, f_signal, name )
% Grafico en tiempo y en frecuencia
%---------Grafico en el tiempo---------------------------------------------
figure('Name',strcat('Señal', name),'NumberTitle','off');
subplot(2,1,1); plot(t_vector,t_signal);        % Grafico de la señal 
%xlim([1.45 1.5])
title(strcat('Grafico de la Señal',name,' en el Tiempo'))
xlabel('Tiempo [s]'); ylabel('Amplitud de la señal [V], x(t)');
%---------Grafico en Frecuencia--------------------------------------------
subplot(2,1,2); plot(f_vector,f_signal);        % Grafico espectro de frecuencia
xlabel('Frecuencia [Hz]'); ylabel('Magnitud, |Fn(f)|');
title(strcat('Grafico de la Señal',name,' en frecuencia'))
end
