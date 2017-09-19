% Tracé sur une même figure des résultats expérimentaux et de simulation.
% Lecture résultat experience Boucle ouverte BO=csvread('mesBOC200mA.csv',1,0) %lecture csv saut premiere ligne
importBF %Import des variables enregistrées avec le générateur automatique MATLAB
dt=2.362/(length(Um)-1);
temps=0:dt:2.362;
% Paramétrage figure
plot(temps,theta,S1.Time,S1.Data)
title('2-D Line Plot')
xlabel('Temps (s)')
ylabel('Vitesse')

