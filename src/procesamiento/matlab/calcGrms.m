%%%%
%%%%
function [ Grms ] = filerDPSD( psd_f, psd_a, K )

N =  length(psd_f);

psd_freq_sub = [];
psd_accel_sub = [];

j = 1;
for i = 1:N
	if mod(i, int16(N/K)) == 0
		psd_freq_sub(j) = psd_f(i);
		psd_accel_sub(j) = psd_a(i);
		j = j + 1;
	end
end

psd_freq = psd_freq_sub;
psd_accel = psd_accel_sub;

%% Calc GRMS Value
areaPSD = 0;
for i = 2:length(psd_freq)
    base = psd_freq(i) - psd_freq(i - 1);
    alt = abs(psd_accel(i)-psd_accel(i - 1));
    m = (log10(psd_accel(i)) - log10(psd_accel(i - 1)))/(log10(psd_freq(i)) - log10(psd_freq(i - 1)));
    offset = psd_accel(i -1) / (psd_freq(i - 1)^m);

    if ~isnan(base) && ~isnan(alt) && ~isnan(m) && ~isnan(offset)

	    if m ~= -1
	    	deltaA = (offset / (m + 1))*(psd_freq(i)^(m+1) - psd_freq(i - 1)^(m+1));
	    	if ~isnan(deltaA)
	        	areaPSD = areaPSD + deltaA;
	        end
	    else
	    	deltaA = offset*(log10(psd_freq(i)) - log10(psd_freq(i - 1)));
	    	if ~isnan(deltaA)
	        	areaPSD = areaPSD + deltaA;
	        end
	    end
	end
end

Grms = sqrt(areaPSD)
GPeak =sqrt(2)*Grms

end