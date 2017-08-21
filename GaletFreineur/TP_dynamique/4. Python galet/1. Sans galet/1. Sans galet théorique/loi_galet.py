import matplotlib.pyplot as plt
import numpy as np

g=100
alpha=(20*2*np.pi)/360


t=np.linspace(0,100,10)
plt.plot(t,g*np.sin(alpha)*t*t/2)

m=2
T=3
plt.plot(t,((m*g*np.sin(alpha)-T)/m)*(t*t/2))



plt.ylabel('postion y')
plt.xlabel('temps t')
plt.show()