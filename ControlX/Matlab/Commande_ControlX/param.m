%-------------------------------------------------------------- 
%Programme servant à définir les constantes utiles aux exemples de pilotage
%et simulation de control'X
%-------------------------------------------------------------- 
    clear all
    clc

    dt=1e-4; %Periode d'échantillonage

%--------------------------------------------------------------    
% Données géométriques
%--------------------------------------------------------------    

    R=155/(2*pi)/1000; % Rayon de la poulie (m) // 155mm : avance par tour de poulie crantée
    i=3;    % Reducteur : Il s'agit d'une réduction !
    
%--------------------------------------------------------------    
% Données propres au moteur
%--------------------------------------------------------------   
    
    r=5.1; %Résistance de l'induit (Ohms)
    L=3.2e-3; %Inductance de l'induit(H)
    kc=0.21; %Constante de couple du moteur (N.m/A)
    ke = 0.2083; % Constante de force contre électromotrice (V/(rad/s))
    k = (kc+ke)/2; %moyenne des deux constantes électromécaniques
    kprim=k*i/R;   %constante de couple du moteur linéaire équivalent
    
%--------------------------------------------------------------    
% Données propres au variateur
%--------------------------------------------------------------   
    
    B=4; %gain pur du variateur de vitesse
    
%--------------------------------------------------------------    
% Données propres à la carte de commande
%-------------------------------------------------------------- 

    Vsat=10; %Tension de saturation carte de commande (volts)

%--------------------------------------------------------------    
% Données expérimentales
%--------------------------------------------------------------   
    Ffrott=28; %Fottement sec ramené sur le chariot :  N 
    fv = 20; % coefficient de frottement visqueux ramenés sur le chariot : N/(m/s)
    Cfrott= Ffrott*R/i; %Frottement sec ramené sur le moteur : N.m
    fw=fv*R^2/i^2;  % Coefficient de frottement visqueux ramené sur le moteur : N.m/(rad/s)

%Moteur linéaire équivalent : remplace tous les blocs élémentaires
    Keq=132;     %(rad/s)/V
    Teq=0.022;   %(s)  
%Tension de seuil du moteur linéaire équivalent (Bande morte)
    useuil=1.5; %Volts
    
%Tf Constante de temps filtre passe bas vitesse (en seconde)
    T=3e-4; 

    meq=3.2; %Inertie de tout l'équipage mobile ramené sur le chariot
    Jeq = meq*R^2/i^2; %Inertie de tout l'équipage mobile ramené sur le moteur

%--------------------------------------------------------------    
% Calibrage de tous les capteurs :
%--------------------------------------------------------------    

%Encodeur incrémental monté sur l'arbre moteur (axe X)
    C=1000*4/(2*pi); %points par radian de rotation de moteur, décodé en *4
    D=R/(i*C)*1000; % en mm/inc
    gain_encodeur_moteur_rad=1/C;
    gain_encodeur_moteur_mm=D;

%Encodeur incrémental monté directement sur le chariot
    gain_regle_mg=-0.04/4; %mm/inc, décodé en *4 : AJUSTER EVENTUELLEMENT LE SIGNE

%Joystick axe X
    gain_joy_X = 5; 
    offset_joy_X = 2.5; % en 

%Joystick axe Y
    gain_joy_Y = 5; 
    offset_joy_Y = 2.5; % en V

%Vitesse axe à partir de la géné tachy
    gain_vitesse_tr_min=1000/6.35; %tr/min de l'arbre moteur
    gain_vitesse_rad_s=1000/6.35*2*pi/60; %rad/s de l'arbre moteur
    gain_vitesse_mm_s=gain_vitesse_tr_min/60*2*pi*R/3*1000; %en mm/s (vitesse chariot)

%Tension moteur axe X
    gain_tension_moteur=5.859; 

%Intensité moteur axe X
    gain_intensite_moteur=2.25;    
    
% capteur de distance Sharp (utilisé dans une "lookup table")
    vecteur_des_distances=[400 350 300 250 200 180 160 140 120 100 90 80 70 60 50 40 30]; %en mm
    vecteur_de_tensions=[0.3 0.37 0.43 0.52 0.65 0.72 0.8 0.92 1.06 1.27 1.4 1.55 1.76 2.02 2.35 2.7 3.05]; %en V

%Capteur d'effort extérieur
    gain_effort_ext=16.36; %en N/V
    offset_effort_ext=16.05;  % en N

%Accéléromètre
    gain_accelero=1/0.174; %en g/V
    
%--------------------------------------------------------------   
    disp ('Paramètres pris en compte')
  