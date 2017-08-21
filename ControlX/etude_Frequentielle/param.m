%--------------------------------------------------------------    
% Control'X
%--------------------------------------------------------------  
    
    clc %efface la fenêtre de commande
    dt=1e-4; %Pas de temps du solveur discret utilisé et période d'échantillonnage en cas de pilotage temps réel
    %dt=1e-3 % Période à choisir dès qu'il y a des blocs StateFlow
%--------------------------------------------------------------    
% Données géométriques
%--------------------------------------------------------------    

    R = 155/(2*pi)/1000; % Rayon de la poulie (m) // 155mm : avance par tour de poulie crantée
    i = 3;    % Reducteur : Il s'agit d'une réduction !
    
%--------------------------------------------------------------    
% Données propres au moteur
%--------------------------------------------------------------   
    
    r = 5.1; %Résistance de l'induit (Ohms)
    L = 3.2e-3; %Inductance de l'induit(H)
    
    kc = 0.21; %Constante de couple du moteur (N.m/A)
    ke = 0.2083; % Constante de force contre électromotrice (V/(rad/s))
    k = (kc+ke)/2; %Moyenne des deux constantes électromécaniques
    
    kprim_c=kc*i/R;%Constante de couple du moteur linéaire éq (N.m/A)
    kprim_e=ke*i/R;% Constante de force contre électromotrice du moteur linéaire éq (V/(rad/s))
    kprim=(kprim_c+kprim_e)/2;%moyenne des deux valeurs précedentes
     
%--------------------------------------------------------------    
% Données propres au variateur
%--------------------------------------------------------------   
    
    B = 4; %gain pur du variateur de vitesse

%--------------------------------------------------------------    
% Résistances passives : Données d'origine expérimentale
%--------------------------------------------------------------   
    Cfrott_moteur = 0.022; % Couple de frottement sec moteur seul
    fw_moteur = 0.124e-3; % Coefficient de frottement visqueux moteur seul

    Ffrott = 28; %Fottement sec de tout l'équipage mobile ramené sur le chariot :  N 
    fv = 20; % Coefficient de frottement visqueux de tout l'équipage mobile ramenés sur le chariot : N/(m/s)
    
    Cfrott = Ffrott*R/i; %Frottement sec ramené sur le moteur : N.m
    fw = fv*R^2/i^2;  % Coefficient de frottement visqueux ramené sur le moteur : N.m/(rad/s)
    
    Vseuil = Cfrott*r/kc; % Moddélisation de l'effort de frottement sec ramené en entrée du moteur : modèle moins fin qu'un effort de frottement sec mais plus souple en terme de simulation numérique : V
 
%--------------------------------------------------------------    
% Données propres à la carte de commande
%--------------------------------------------------------------  
    
    Vsat = 10;     %Tension de saturation : Volts
  
%--------------------------------------------------------------    
% Données propres à la chaîne de retour
% Encodeur incrémental monté sur l'arbre moteur (axe X)
%--------------------------------------------------------------  
    
    C=1000*4/(2*pi); %points par radian de rotation de moteur, décodé en *4
    D=R/(i*C)*1000; % en mm/inc     
        
%--------------------------------------------------------------      
%Détail du calcul de méq
%-------------------------------------------------------------- 

Jmot=0.037e-3+0.012e-3+8e-8; %Moteur+géné tachy + encodeur
I1=Jmot;
Ir=0.135e-4; % Réducteur ramené sur l'entrée
I2roulement=2*(8.349e-6+18*7/20*0.82e-3*19.5e-3^2*18); %2 bagues int de roulement à billes + billes montées sur  poulie crantée
I3=4.2e-5+0.09e-4+0.013e-4+0.15e-4+I2roulement; % Poulie + accouplement (2 parties) + bagues int de roulement à billes
m4=0.16; % Courroie
m5=0.9+0.525+0.2;% Chariot avec accessoires
I6=4.2e-5+0.01e-4+I2roulement; %Poulie crantée + bague int de roulement à billes

Jeq=I1+Ir+1/i^2*(I3+I6+(m4+m5)*R^2); % Inertie ramenée sur le moteur (kg.m2)
meq=Jeq*i^2/R^2; % Inertie ramenée sur le chariot (kg)


%--------------------------------------------------------------      
%Effort extérieur
%-------------------------------------------------------------- 

Fext = 0; % Un éventuel effort extérieur (N)

disp ('Paramètres pris en compte')