

%% Initialisation carte E/S
clear all
d= daq.getDevices;
if d.isvalid == 0
    disp(' --- ERREUR --- Pas de carte E/S disponible')
    break
end
sprintf('Le système dispose de %d adaptateurs',size(d,2))


s = daq.createSession('ni')
s.addAnalogInputChannel('dev1','ai0','voltage')
s.addAnalogInputChannel('dev1','ai1','voltage')

%% 
disp( 'Début programme')

data = startForeground(s);
plot (data);

%% Fin programme
%release(s)

    
    