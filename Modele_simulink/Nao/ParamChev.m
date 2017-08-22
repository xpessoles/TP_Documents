%% Paramètres modèle

% Couple extérieur (la gravité pourrait être prise en compte)
Cext=0

%% Constantes pour la cheville du robot

%% Caractéristiques du moteur (S.I.)
R=5.4
L=0%0.6E-3
Jmot=4.8E-7 %kg.m² chateau : 4.8E-8
Ke=0.0194 % V/(rad/s)
Ki=0.0194 % N.m/A
f= 1.6E-5 %N.m/(rad/s)
% Rapport de réduction
k=13*25*12*10/(80*47*58*36)
% Tension alimentation
Vbat=24 %V

%% Inertie
% Inertie cheville nue
Jch0=0
% Inertie ajoutée
% Inertie support
Jsup=0
% Masse ajoutée
m=0
% Distance masse a l'axe de rotation
d=0
% Inertie cheville chargée
Jch=Jch0+Jsup+m*d^2
% Alternative :
% 1/2 NAO "nez creux" Cg: environ 35cm poids 5.2kg Icg = 5.2*0.35^2 = 0.53
% Ibarreeq: 5.2 * 0.57^2 / 12 = 0.14 Jtot = 0.67 sur axemot : 
Jch = 0.63 / 2 % /2 demi nao
% Finalement
% Inertie équivalente ramenée à l'axe moteur
Jeq = Jmot + Jch*k^2
