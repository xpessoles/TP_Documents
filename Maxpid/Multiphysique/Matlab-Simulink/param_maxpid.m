% POIDS
g=10
Ray=0.3        % rayon du bras
m=1            % masse en bout de bras
% PARTIE OPERATIVE
Kve=4/2/3.14;  % Gain vis-écrou (en mm/rad)
Kmeca=0.84;    % Gain syst méca (en deg/mm)
% MOTEUR
Ke=52.5e-3     % Couplage magnétique
R= 2.07        % Résistance moteur
L=0.62e-3      % inductance moteur
J=70e-7+ m*(Ray*Kve*Kmeca*3.14/180)^2       % Inertie moteur
% PARTIE COMMANDE
Kpot=5/95;  % gain potentiometre (en V/deg)
KCAN=255/5  % Gain convertisseur AN
K1=Kpot*KCAN;
Kh=21.1/255/0.9   % Gain hacheur (21.1V pour 90% de la consigne max)
Kp=30
Ki=0
Kd=0
