close all
% Tracé sur une même figure des résultats expérimentaux et de simulation. saut premiere ligne
import1 %Import des variables enregistrées avec le générateur automatique MATLAB
dt=2.4/(length(Um)-1);
temps=0:dt:2.4;
% Paramétrage figure
plot(temps,theta,'r-','LineWidth',3)
hold on
plot(S1.Time,S1.Data,'b--','LineWidth',3)
plot(temps,Um,'g-','LineWidth',3)
plot(temps,Im,'m-','LineWidth',3)
title('2-D Line Plot')
xlabel('Temps (s)')
ylabel('\theta(t) (en °)')
legend('Essai expérimental','Simulation','Tension','Intensité')

