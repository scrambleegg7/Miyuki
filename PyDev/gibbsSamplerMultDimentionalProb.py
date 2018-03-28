
from math import *
from matplotlib.pylab import * 
import numpy as np

# 3d plot with iteration as z axis
from mpl_toolkits.mplot3d import Axes3D


n=100
rho=.99 #correlation
#Means
m1 = 10
m2 = 20
#Standard deviations
s1 = 1
s2 = 1
#Initialize vectors
x = np.array([0.] * n)
y = np.array([0.] * n)

sd=sqrt(1-rho**2)
# the core of the method: sample recursively from two normal distributions
# Tthe mean for the current sample, is updated at each step.
for i in range(1,n):
  x[i] = normal(m1+rho*(y[i-1]-m2)/s2,s1*sd)
  y[i] = normal(m2+rho*(x[i-1]-m1)/s1,s2*sd)

scatter(x,y,marker='d',c='r')
title('Amostrador de Gibbs')
xlabel('x')
ylabel('y')
grid()

fig = figure()
ax = Axes3D(fig)
ax.plot(x, y, range(len(x)))
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('n')



show()