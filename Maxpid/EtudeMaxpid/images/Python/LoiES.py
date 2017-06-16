# -*- coding: utf-8 -*-
"""
Created on Mon Feb  2 21:49:38 2015

@author: Xavier
"""

import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
import math

a,b,c,d = 106.3, 59, 70, 80
p = 4

gamma = np.linspace(0,40*math.pi,1000)
dgamma = np.ones(1000)


dtheta = -(((np.sqrt(d*d+c*c+b*b+2*b*c)-p*gamma/(2*math.pi))*(-p*dgamma/(2*math.pi)))/(a*b))/(np.sqrt(1-((((np.sqrt(d*d+c*c+b*b+2*b*c)-p*gamma/(2*math.pi))**2)-a*a-b*b)/(2*a*b))**2))

theta = np.arccos((((np.sqrt(d*d+c*c+b*b+2*b*c)-p*gamma/(2*math.pi))**2)-a*a-b*b)/(2*a*b))-np.arctan(d/c)
theta = theta*360/(2*math.pi)

slope, intercept, r_value, p_value, std_err = stats.linregress(gamma,theta)
regress = slope*gamma + intercept
titre = str(slope)+"gamma"+str(intercept)


plt.plot(gamma,theta)
plt.plot(gamma,regress)
plt.xlabel("$\\gamma$")
plt.ylabel("$\\theta$")
plt.legend(("Modèle","Régression linéaire - $0,696 \gamma + 6,098$"),'best')
plt.grid()

from matplotlib2tikz import save as tikz_save