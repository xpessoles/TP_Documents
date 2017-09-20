% Tracé sur une même figure des résultats expérimentaux et de simulation. saut premiere ligne
filenames={'essai_pos1_kp1000000.csv';'essai_pos2_kp1000000.csv'};

for k=1:length(filenames)
    filename=sprintf('essais/%s',filenames{k});
    dataArray=import_file(filename);
    theta{:,k} = dataArray{:, 1};
    Um{:,k} = dataArray{:, 2};
    omega{:,k} = dataArray{:, 3};
    Im{:,k} = dataArray{:, 4};
    dt=2.4/(length(Um{:,k})-1);
    temps{:,k}=0:dt:2.4;
    leg{1,k}=sprintf('Experience en configuration %d',k);
end

hold on
for k=1:length(filenames)
    plot(temps{:,k},theta{:,k},'--')
end
% Parametrage figure
plot(S1.Time,S1.Data,'LineWidth',3)%Kp=1E6
leg{1,k+1}='Simulation en configuration 1';
plot(S4.Time,S4.Data,'LineWidth',3)%Kp=1E5
leg{1,k+2}='Simulation en configuration 2';
xlabel('Temps (s)')
ylabel('\theta(t) (en °)')
legend(leg)

