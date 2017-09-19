clear all
close all
scrsz = get(0,'ScreenSize');

wf=9/10;
hf=4/5;
figsize=[0 0  0.9*scrsz(3) 0.9*scrsz(4)];
%Calcul de la fonction de transfert
%---------------------------------------

%Importation de la fonction du diagramme de Bode experimental
import_bode;
w_exp=freq*1e-3*2*pi;
gain_exp=gain;
phase_exp=phase

figure1=figure('position',figsize);
axes1=subplot(2,1,1,'parent',figure1,'YGrid','on',...
    'XScale','log',...
    'XMinorTick','on',...
    'XMinorGrid','on',...
    'XGrid','on',...
    'fontsize',20);
box(axes1,'on');
hold(axes1,'all');


semilogx(w_exp,gain_exp,'b*-','linewidth',2)


% xlim([10^0 10^3])
% ylim([-60 20])

xlabel('$\omega (rad\cdot s^{-1})$','fontsize',25,'interpreter','latex');
ylabel('$G (dB)$','fontsize',25,'interpreter','latex');

axes2=subplot(2,1,2,'parent',figure1,'ygrid','on',...
    'xscale','log',...
    'xminortick','on',...
    'xminorgrid','on',...
    'xgrid','on',...
  'fontsize',20);
box(axes2,'on');
hold(axes2,'all');



semilogx(w_exp,phase_exp,'b*-','linewidth',3)


% xlim([10^0 10^3])
% ylim([-190 100])


xlabel('$\omega (rad\cdot s^{-1})$','fontsize',25,'interpreter','latex');
ylabel('$\varphi (^{\circ})$','fontsize',25,'interpreter','latex');


