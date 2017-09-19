% Tracé sur une même figure des résultats expérimentaux et de simulation. saut premiere ligne
filenames={'essai_pos1_kp1000000.csv';'essai_pos1_kp100000.csv';'essai_pos1_kp50000.csv'};
vKp=[1e6,1e5,5*1e4];
for k=1:length(filenames)
    filename=sprintf('essais/%s',filenames{k});
    dataArray=import_file(filename);
    theta{:,k} = dataArray{:, 1};
    Um{:,k} = dataArray{:, 2};
    omega{:,k} = dataArray{:, 3};
    Im{:,k} = dataArray{:, 4};
    dt=2.4/(length(Um{:,k})-1);
    temps{:,k}=0:dt:2.4;
    leg{1,k}=sprintf('Experience avec K_p= %d',vKp(k));
end

hold on
for k=1:length(filenames)
    plot(temps{:,k},theta{:,k},'--')
end
% Parametrage figure
plot(S1.Time,S1.Data,'LineWidth',3)%Kp=1E6
leg{1,k+1}=sprintf('Simulation avec K_p= %d',vKp(1));
plot(S2.Time,S2.Data,'LineWidth',3)%Kp=1E5
leg{1,k+2}=sprintf('Simulation avec K_p= %d',vKp(2));
plot(S3.Time,S3.Data,'LineWidth',3)%Kp=1E5
leg{1,k+3}=sprintf('Simulation avec K_p= %d',vKp(3));
line([0 2.5],[31.5 31.5],'color','k','linestyle','--','linewidth',1)
line([0 2.5],[28.5 28.5],'color','k','linestyle','--','linewidth',1)
line([0 2.5],[30 30],'color','k','linestyle','--','linewidth',1)
xlabel('Temps (s)')
ylabel('\theta(t) (en °)')
legend(leg)

