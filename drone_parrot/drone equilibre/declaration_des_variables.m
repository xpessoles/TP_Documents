%------déclaration des variables------
%-------------------------------------

%------paramétre(s) des moteurs à courant continu------
%résistance interne
Rm=1e-1    %0.1
%inductance du bobinage
Lm=1e-3  %0.001
Cond=0
%constante de force electromotrice
Km=9/(28500*pi/30)

%------paramétre(s) des réducteurs------
%rapport de transformation E/S
k=69/8

%------paramètres de l'hélice------
%coefficient de couple de lacet
Coef_C=-(0.01)/(28500*pi/(k*30))^2
%coefficient de portance
Coef_P=-(9.81*0.09)/(28500*pi/(k*30))^2

%------consignes-------------------
C=9.038 ;
C1=C ;
C2=C ;
C3=-C ;
C4=-C ;
