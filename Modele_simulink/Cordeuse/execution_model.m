clear all; % effacement de la mémoire
close all; % fermeture de toutes les fenêtres
clc; % effacement de la fenetre commande

para %execution du fichier paramètres


    
figure('Color',[1,1,1]) % création du figure vide à fond blanc   
for i=1:2   
    Ka=Ka*2; % changer valeur du paramètre voulu ici 
      
    sim('modele_cordeuse')  % execution du modèle simulink

% extraction des données simulink (il faut cocher log signal data) au préalable sur le signal à visualiser    
    T1 = logsout.getElement('T1').Values.Data;   % extraction de la donnée simulink
    t = logsout.getElement('T1').Values.time;

    plot(t,T1)
    hold on % pour pouvoir tracer plusieurs courbes
end
grid on;box on;

% créer légende
% créer label d'axes


  %set_param('modele_cordeuse','SimulationCommand','start')  % exécution
    %pour garder la main