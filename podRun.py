from scipy.integrate import odeint
from scipy.special import gamma, airy
from numpy import arange
from EddyBrake import EddyBrake
import numpy as np
import pandas as pd

import matplotlib.pyplot as plt

m_pod = 385.0 #kg
c_d = 0.35 # m^2
frontal_area = 1.14 # m^2

eddyBrake = EddyBrake('./eddyBrakeData.csv')

x_0 = 0.0 # pod initial position
v_0 = 99.0 # pod initial velocity

def pusherForce(t):
  f = 10000.0
  if t > 0:
    f = 0.0
  return f

def railTemp(q):
  # Thermodynamics, An Engineering Approach
  # rho_al = 2700. kg/m^3
  # c_al = 0.902 kJ/(kg*K) @ 300K
  c = 902.0
  rho = 2700.0
  Ti = 40.0 
  l = 0.10795*6.0
  return l*q/(v*q*c*rho) + Ti

def dragForce(v):
  #return -0.5*frontal_area*c_d*v**2  
  return 0.0

y0 = [x_0, v_0]

def func(y, t):
  a = ( 
       -12.0*eddyBrake.f_drag(y[1],0.001)
       +dragForce(y[1])
       +pusherForce(t)
      )/m_pod
  return [y[1],a]

x = arange(0, 120, 0.01)
t = x
y = odeint(func, y0, t)

# calc aux fields
T_final = np.zeros(len(t))
H_y_max = np.zeros(len(t))
H_y_mean = np.zeros(len(t))

for i in range(len(t)):
  #h = h[i]
  h = 0.001
  v = y[i,1]
  print('Warning: hard coded h value!!!')
  T_final[i] = railTemp(eddyBrake.q_max(v,h))
  H_y_max[i] = eddyBrake.H_y_max(v,h)
  H_y_mean[i] = eddyBrake.H_y_mean(v,h)

df_out = pd.DataFrame({
    'time [s]':t,
    'position [m]':y[:,0],
    'velocity [m\s]':y[:,1],
    'T_rail_final [C]':T_final,
    'H_y_max':H_y_max,
    'H_y_mean':H_y_mean
    })

df_out.to_csv('out.csv')

# output

plt.figure()

plt.subplot(411)
plt.plot(t,y[:,0])
plt.xlabel('time [s]')
plt.ylabel('position [m]')
plt.grid()

plt.subplot(412)
plt.plot(t,y[:,1])
plt.xlabel('time [s]')
plt.ylabel('velocity [m/s]')
plt.grid()

plt.subplot(413)
plt.plot(t,H_y_max,label='max')
plt.plot(t,H_y_mean,label='mean')
plt.xlabel('time [s]')
plt.ylabel('H_y [A/m]')
plt.legend(loc='lower left')
plt.grid()

plt.subplot(414)
plt.plot(t,T_final)
plt.xlabel('time [s]')
plt.ylabel('I-beam\nbounding temp [C]')
plt.grid()

plt.show()
