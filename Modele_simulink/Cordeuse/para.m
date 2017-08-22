% paramètres pour le modèle simulink de la cordeuse

eta = 29*55/(2*15) ; % 1/rapport de réduction 
K11 = 9e-6 ; % V/N gain du capteur "d'effort"
R = 20e-3; % rayon de la poulie
Rm = 2; % en Ohm, resistance électrique du moteur
Lm = 1e-3; % inductance du moteur en H
Meq = 500; % masse equivalente ramenée au moteur
K = 27e3;  % raideur du ressort (capteur) en N/m
k = 4e3;   % raideur de la corde en N/m
Ke = 0.032 ; % gain de FEM en V.s
Ki = 0.032 ; % constante de couple en Nm/A
f = 0.28 ; % coefficient de frottement

Kp = 1000 ; % gain du correcteur proportionnel
Ki = 2000 ; % gain du correcteur intégral
Kd = 0 ; % gain du correcteur dérivé




