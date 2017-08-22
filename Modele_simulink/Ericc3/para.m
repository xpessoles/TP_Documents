% Paramètres modèle

% Moteur CC
Kc = 0.042 ; %constante de couple (Nm/A)
Jeq=2.9e-5 ; %inertie équivalente ramenée au moteur (kg.m²)
f =8.06e-5 ; %coefficient de frottement visqueux total ramené à l'arbre moteur (NM/(rad/s))
Cfsec=1 ; %couple de frottement sec s'opposant au mvt (Nm)

% Correcteur PID
Kp=1000;  
Ki=0 ; 
Kd=0;

DAC=1