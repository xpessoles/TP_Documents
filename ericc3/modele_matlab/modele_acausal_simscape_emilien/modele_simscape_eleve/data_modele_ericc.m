%Conversion analogique numerique
KAN=2*1e6/1080;

%Capteur (codeur incremental)
Kc=2000/(2*pi);

%Parametres du correcteur
Kp=1e6;
Ki=0;
Kd=0;

%Reducteur
Kr=3/1000;

%Parametres du moteur
Kv=0.17;
Kt=0.043;
Ke=0.043;
Jm=0.41*1e-5;
R=2.3;
L=1.1*1e-3;
fv=1e-4;
Jeq=2.09*1e-5;

%Inertie du robot
J1=1.76*1E3;
J2=2.44*1E3;
Jeq1=J1*Kr^2;
Jeq2=J2*Kr^2;
r=Jeq2/Jeq1;

%Perturbation
Cr=0.0;

%Gain d'adaptation de sortie
Ks=Kc/(Kr*KAN);
