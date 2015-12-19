from scipy.integrate import odeint
from scipy.special import gamma, airy
from numpy import arange

import matplotlib.pyplot as plt

m_pod = 2500.0 #kg
c_d = 0.4 # m^2
frontal_area = 0.785 # m^2

x_0 = 0 # pod initial position
v_0 = 0 # pod initial velocity

def pusherForce(t):
  f = 10000.0
  if t > 10:
    f = 0.0
  return f

def brakeForce(t,v):
  if t<20 or v<=0:
    return 0
  else:
    return -10000.0

def dragForce(v):
  return -0.5*frontal_area*c_d*v**2  

y0 = [x_0, v_0]

def func(y, t):
  a = (pusherForce(t)+brakeForce(t,y[1])+dragForce(y[1]))/m_pod
  return [y[1],a]

x = arange(0, 30, 0.01)
t = x
y = odeint(func, y0, t)

plt.figure()
plt.plot(t,y[:,0])
plt.xlabel('time [s]')
plt.ylabel('Hyperpod position [m]')
plt.grid()

plt.figure()
plt.plot(t,y[:,1])
plt.xlabel('time [s]')
plt.ylabel('Hyperpod velocity [m/s]')
plt.grid()

plt.show()



