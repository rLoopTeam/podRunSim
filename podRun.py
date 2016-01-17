from scipy.integrate import ode
from scipy.special import gamma, airy
from numpy import arange
from EddyBrake import EddyBrake
import numpy as np
import pandas as pd

import matplotlib.pyplot as plt

# inputs
##########
m_pod = 385.0 #kg 
c_d = 0.35 # m^2 
frontal_area = 1.14 # m^2

eddyBrakeDataFile = './eddyBrakeData.csv'
n_mag_fea = 2.0
n_mag_drag = 24.0
n_mag_lift = 12.0
n_mag_thermal = 12.0

t_max = 120.0 #seconds
t0 = 0.0 

T_rail_init = 40.0

x_0 = 0.0 # pod initial position
v_0 = 99.0 # pod initial velocity

dt_outer = 0.01
outfile = 'out.csv'
##########

def pusherForce(t):
  f = 10000.0
  if t > 0:
    f = 0.0
  return f

def railTemp(q,v,Ti):
  # Thermodynamics, An Engineering Approach
  # rho_al = 2700. kg/m^3
  # c_al = 0.902 kJ/(kg*K) @ 300K
  c = 902.0
  rho = 2700.0
  Ti = 40.0 
  l = 0.10795*n_mag_thermal/n_mag_fea
  return l*q/(v*c*rho) + Ti

def dragForce(v):
  #return -0.5*frontal_area*c_d*v**2  
  return 0.0

class piController():

  def __init__(self,):
    self.i = 0
    self.a_set = -0.5*9.81
    self.k_i = 0.01
    self.k_p = 0.001
    self.t = 0
  
  def evaluate(self,t,a):
    self.t_old = self.t
    self.t = t
    error = a - self.a_set
    self.i += error*(self.t-self.t_old)
    if abs(self.i)>1000:
      self.i = self.i/abs(self.i)*1000
    h = 0.1-(self.k_i * self.i + self.k_p * error)

    if h > 0.020:
      h = 0.020
    if h < 0.001:
      h = 0.001

    return h

class PodModel():

  def __init__(self,m_pod):
    self.t = 0
    self.t_old = 0
    self.v = 0
    self.v_old = 0
    self.x = 0
    self.x_older = 0
    self.h = 0.001
    self.m_pod = m_pod
    self.a = 0

  def setICs(self,y,t):
    self.t = t
    self.t_old = t
    self.v = y[1]
    self.v_old = y[1] 
    self.x = y[0]
    self.x_older = y[0]

  def setEddyBrakeModel(self,model):
    self.eddyBrake = model

  def on_control_loop_timestep(self,h):
    self.h = h
    return None

  def on_integrator_timestep(self,t,y):
    self.t_old = self.t
    self.t = t
    self.v_old = self.v
    self.v = y[1]
    self.x_old = self.x
    self.x = y[0]
    self.a = (self.v - self.v_old)/(self.t-self.t_old)
    # update any coeffecients if needed
    # for example the current rail temp could be calculated
    # here, but now it's purely an output so it's not needed,
    # but if a radiation model were implemented, we'd need to
    # calculate it here. For example:
    #self.T_final = railTemp(eddyBrake.q_max(v,h))
    return None

  def y_dot(self,t,y):
    x = y[0]
    v = y[1]
    a = -n_mag_drag/n_mag_fea*self.eddyBrake.f_drag(v,self.h)/self.m_pod
    return [v,a]
  

t = arange(0, t_max, dt_outer)

# allocate state variables
x = np.ones(len(t))*np.nan
v = np.ones(len(t))*np.nan
a = np.ones(len(t))*np.nan

# allocate aux fields
T_final = np.ones(len(t))*np.nan
H_y_max = np.ones(len(t))*np.nan
H_y_mean = np.ones(len(t))*np.nan
accel_g = np.ones(len(t))*np.nan
lift_per_assy = np.ones(len(t))*np.nan
gap = np.ones(len(t))*np.nan


# create state vector for t0
y0 = [x_0, v_0]

# initialize model
eddyBrake = EddyBrake(eddyBrakeDataFile)
model = PodModel(m_pod)
model.setEddyBrakeModel(eddyBrake)
model.setICs(y0,t0)

controller = piController()

# store state vars for t0
x[0] = x_0
v[0] = v_0
a[0] = 0.0

# evaluate aux variables for t0
T_final[0] = railTemp(eddyBrake.q_max(model.v,model.h).max(),model.v,T_rail_init)
H_y_max[0] = eddyBrake.H_y_max(model.v,model.h)
H_y_mean[0] = eddyBrake.H_y_mean(model.v,model.h)
lift_per_assy[0] = n_mag_lift/n_mag_fea*eddyBrake.f_lift(model.v,model.h)
accel_g[0] = 0
gap[0] = model.h

r = ode(model.y_dot).set_integrator("dopri5")
r.set_solout(model.on_integrator_timestep)
r.set_initial_value(y0, t0)

i=0
while r.successful() and r.t<t_max:
  r.integrate(r.t+dt_outer)
  print('time: {}, velocity: {}'.format(r.t,model.v))
  i+=1
  #h = 0.020 * 0.5 * np.sin(np.pi*r.t/5.) + 0.012 
  h = controller.evaluate(r.t,model.a)
  model.on_control_loop_timestep(h)

  x[i] = r.y[0]
  v[i] = r.y[1]
  a[i] = model.a

  # Evaluate aux variables here that are only for output.
  # Calc them in model.on_timestep if the state model
  # depends them, but assign them to the output arrays here.
  T_final[i] = railTemp(eddyBrake.q_max(v[i],model.h),model.v,T_rail_init)
  #T_final[i] = model.T_final # if state model needs T_final
  H_y_max[i] = eddyBrake.H_y_max(v[i],model.h)
  H_y_mean[i] = eddyBrake.H_y_mean(v[i],model.h)
  lift_per_assy[i] = n_mag_lift/n_mag_fea*eddyBrake.f_lift(v[i],model.h)
  accel_g[i] = model.a/9.81
  gap[i] = model.h

# output

df_out = pd.DataFrame({
    'time [s]':t,
    'position [m]':x,
    'velocity [m\s]':v,
    'T_rail_final [C]':T_final,
    'H_y_max':H_y_max,
    'H_y_mean':H_y_mean,
    'accel [g]':accel_g,
    'gap [m]':h
    })

df_out.to_csv(outfile)


plt.figure()

plt.subplot(711)
plt.plot(t,x)
plt.xlabel('time [s]')
plt.ylabel('position [m]')
plt.grid()

plt.subplot(712)
plt.plot(t,v)
plt.xlabel('time [s]')
plt.ylabel('velocity [m/s]')
plt.grid()

plt.subplot(713)
plt.plot(t,accel_g)
plt.xlabel('time [s]')
plt.ylabel('accel [g]')
plt.grid()

plt.subplot(714)
plt.plot(t,H_y_max,label='max')
plt.plot(t,H_y_mean,label='mean')
plt.xlabel('time [s]')
plt.ylabel('H_y [A/m]')
plt.legend(loc='lower left')
plt.grid()

plt.subplot(715)
plt.plot(t,T_final)
plt.xlabel('time [s]')
plt.ylabel('T_ibeam_surf [C]')
plt.grid()

plt.subplot(716)
plt.plot(t,lift_per_assy)
plt.xlabel('time [s]')
plt.ylabel('F_lift_per_side [N]')
plt.grid()

plt.subplot(717)
plt.plot(t,gap)
plt.xlabel('time [s]')
plt.ylabel('gap [m]')
plt.grid()

plt.show()
