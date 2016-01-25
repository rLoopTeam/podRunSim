from scipy.integrate import ode
from scipy.special import gamma, airy
from numpy import arange
from EddyBrake import EddyBrake
import numpy as np
import pandas as pd
import argparse
import matplotlib.pyplot as plt
import json
from scipy.optimize import minimize_scalar
from scipy.interpolate import interp1d

parser = argparse.ArgumentParser()
parser.add_argument('infile',help='input file')
args = parser.parse_args() 

f = open(args.infile)
raw = f.read()
f.close

inputs = json.loads(raw)

# inputs
##########
m_pod = inputs['m_pod'] #kg 
eddyBrakeDataFile = inputs['eddyBrakeDataFile']
n_mag_fea = inputs['n_mag_fea']
n_mag_drag = inputs['n_mag_drag']
n_mag_lift = inputs['n_mag_lift']
n_mag_thermal = inputs['n_mag_thermal']

t_max = inputs['t_max'] #seconds
t0 = inputs['t0']

T_rail_init = inputs['T_rail_init']

x_0 = inputs['x_0'] # pod initial position
v_0 = inputs['v_0'] # pod initial velocity

dt_outer = inputs['dt_outer']
outfile = inputs['outfile']

brakeControllerDict = inputs['brakeController']
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
  l = 0.10795*n_mag_thermal/n_mag_fea
  return l*q/(v*c*rho) + Ti

def dragForce(v):
  #return -0.5*frontal_area*c_d*v**2  
  return 0.0

class piController():

  def __init__(self,params):
    self.i = 0
    self.a_set = -params['decel_target']*9.81
    self.k_i = params['k_i']
    self.k_p = params['k_p']
    self.gap_max = params['gap_max']
    self.gap_min = params['gap_min']
    self.t = 0
  
  def evaluate(self,t,a,v,x):
    self.t_old = self.t
    self.t = t
    error = a - self.a_set
    self.i += error*(self.t-self.t_old)
    if abs(self.i)>1000:
      self.i = self.i/abs(self.i)*1000
    h = self.gap_max - (self.gap_max-self.gap_min)*(self.k_i * self.i + self.k_p * error)

    if h > self.gap_max:
      h = self.gap_max
    if h < self.gap_min:
      h = self.gap_min

    return h,0

class constantGapBrakeController():

  def __init__(self,params):
    self.gap = params['gap']

  def evaluate(self,t,a,v,x):
    return self.gap,0

class constDecelLookupTableController():

  def __init__(self,params,m_pod,eddyBrake,n_mag_fea,n_mag_drag):
    self.eb = eddyBrake
    self.n_mag_fea = n_mag_fea
    self.n_mag_drag = n_mag_drag
    self.a_set = params['decel_target']*9.81
    self.gap_max = params['gap_max']
    self.gap_min = params['gap_min']
    self.m_pod = m_pod
    #self.v = 10.0

  def evaluate(self,t,a,v,x):
    #self.v = v
    h = minimize_scalar(self.func,method='Bounded',
             bounds=[self.gap_min,self.gap_max],args=(v,)).x
    return h,0

  def func(self,h,v):
    return (self.n_mag_drag/self.n_mag_fea*self.eb.f_drag(v,h).max()/self.m_pod-self.a_set)**2.0

class trajectoryPlanController():

  def __init__(self,params,m_pod,eddyBrake,n_mag_fea,n_mag_drag):
    self.eb = eddyBrake
    self.n_mag_fea = n_mag_fea
    self.n_mag_drag = n_mag_drag
    self.m_pod = m_pod
    
    self.state = 'accel'

    self.gap_max = params['gap_max']
    self.gap_min = params['gap_min']

    self.xMaxAccel = params['xMaxAccel']
    self.xMax = params['xMax']
    self.vMax = params['vMax']
    self.accel = params['accel']*9.81
    self.brakingMode = params['brakingMode']

    self.lutc =  constDecelLookupTableController(params,m_pod,eddyBrake,n_mag_fea,n_mag_drag)

    df = pd.read_csv(params['brakingCurve'])
    df = df[df['velocity [m/s]'].isnull() == False]
    df = df.sort(['velocity [m/s]'])
    self.brakeCurveDispAtSpeed = interp1d(df['velocity [m/s]'],df['position [m]'])
    self.brakeCurveMaxDisp = df['position [m]'].max()
    self.brakeCurveAccelAtSpeed = interp1d(df['velocity [m/s]'],df['accel [g]'])
    self.brakeCurveGapAtPosition = interp1d(df['position [m]'],df['gap [m]'])

  def evaluate(self,t,a,v,x):

    if self.state == 'accel':
      if (v >= self.vMax) or (x >= self.xMaxAccel):
        self.state = 'coast'
        print('accel->coast')
      if self.itsTimeToStartBraking(v,x):
        self.state = 'brake'
        self.brakingCurveOffset = x
        print('accel->brake')
      thrust = self.m_pod*self.accel
      h = self.gap_max

    if self.state == 'coast':
      if self.itsTimeToStartBraking(v,x):
        self.state = 'brake'
        self.brakingCurveOffset = x
        print('coast->brake')
      thrust = 0
      h = self.gap_max

    if self.state == 'brake':
      if self.brakingMode == 'minGap':
        h = self.gap_min
        thrust = 0
      elif self.brakingMode == 'gapVsPosition':
        h = self.brakeCurveGapAtPosition(x-self.brakingCurveOffset)
        # needs work, not correct               ^
        thrust = 0
      else:
        raise Warning("brakingMode was not specified in brakeController params")

    return h,thrust

  def itsTimeToStartBraking(self,v,currentPosition):
    stoppingDistanceNeeded = self.brakeCurveMaxDisp - self.brakeCurveDispAtSpeed(v)
    if (currentPosition + stoppingDistanceNeeded) > self.xMax:
      return True
    else:
      return False

class percentOfMaxBrakingForceController():

  def __init__(self,params,m_pod,eddyBrake,n_mag_fea,n_mag_drag):
    self.gap_min = params['gap_min']
    self.gap_max = params['gap_max']
    self.eddyBrake = eddyBrake
    self.percentage = params['percentage']

  def evaluate(self,t,a,v,x):
    f_max = self.eddyBrake.f_drag(v,self.gap_min)
    f_requested = f_max * self.percentage/100.
    h = minimize_scalar(self.func,method='Bounded',
             bounds=[self.gap_min,self.gap_max],args=(v,f_requested)).x
    return h,0

  def func(self,h,v,f):
    return (self.eddyBrake.f_drag(v,h)-f)**2

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
    self.thrust = 0

  def setICs(self,y,t):
    self.t = t
    self.t_old = t
    self.v = y[1]
    self.v_old = y[1] 
    self.x = y[0]
    self.x_older = y[0]

  def setEddyBrakeModel(self,model):
    self.eddyBrake = model

  def on_control_loop_timestep(self,h,thrust):
    self.h = h
    self.thrust = thrust
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
    a = (self.thrust
         -n_mag_drag/n_mag_fea*self.eddyBrake.f_drag(v,self.h)
        )/self.m_pod
    return [v,a]
  

t = arange(0, t_max, dt_outer)
n_outerSteps = t_max/dt_outer

# allocate state variables
t = np.ones(n_outerSteps+1)*np.nan
x = np.ones(n_outerSteps+1)*np.nan
v = np.ones(n_outerSteps+1)*np.nan
a = np.ones(n_outerSteps+1)*np.nan

# allocate aux fields
T_final = np.ones(n_outerSteps+1)*np.nan
H_y_max = np.ones(n_outerSteps+1)*np.nan
H_y_mean = np.ones(n_outerSteps+1)*np.nan
accel_g = np.ones(n_outerSteps+1)*np.nan
lift_per_assy = np.ones(n_outerSteps+1)*np.nan
gap = np.ones(n_outerSteps+1)*np.nan


# create state vector for t0
y0 = [x_0, v_0]

# initialize model
eddyBrake = EddyBrake(eddyBrakeDataFile)
model = PodModel(m_pod)
model.setEddyBrakeModel(eddyBrake)
model.setICs(y0,t0)

# instanciate brake controller
if brakeControllerDict['type'] == 'piController':
  controller = piController(brakeControllerDict['params'])
elif brakeControllerDict['type'] == 'constant_gap':
  controller = constantGapBrakeController(brakeControllerDict['params'])
elif brakeControllerDict['type'] == 'constDecelLookupTable': 
  controller = constDecelLookupTableController(brakeControllerDict['params'],m_pod,eddyBrake,n_mag_fea,n_mag_drag)
elif brakeControllerDict['type'] == 'trajectoryPlanController':
  controller = trajectoryPlanController(brakeControllerDict['params'],m_pod,eddyBrake,n_mag_fea,n_mag_drag)
elif brakeControllerDict['type'] == 'percentOfMaxBrakingForceController':
  controller = percentOfMaxBrakingForceController(brakeControllerDict['params'],m_pod,eddyBrake,n_mag_fea,n_mag_drag)
else:
  raise Warning('no brake controller specified')

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

h,thrust = controller.evaluate(t[0],a[0],v_0,x_0)
model.on_control_loop_timestep(h,thrust)

i=0
while r.successful() and i<n_outerSteps:
  r.integrate(r.t+dt_outer)
  print('time: {}, velocity: {}'.format(r.t,model.v))
  i+=1
  h,thrust = controller.evaluate(r.t,model.a,model.v,model.x)
  model.on_control_loop_timestep(h,thrust)

  t[i] = r.t
  x[i] = r.y[0]
  v[i] = r.y[1]
  a[i] = model.a

  # Evaluate aux variables here that are only for output.
  # Calc them in model.on_timestep if the state model
  # depends them, but assign them to the output arrays here.
  T_final[i] = railTemp(eddyBrake.q_max(v[i],model.h).max(),model.v,T_rail_init)
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
    'velocity [m/s]':v,
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
plt.ylabel('H [A/m]')
plt.legend(loc='lower left')
plt.grid()

plt.subplot(715)
plt.plot(t,T_final)
plt.xlabel('time [s]')
plt.ylabel('$\Delta$T I-beam\nsurface [C]')
plt.grid()

plt.subplot(716)
plt.plot(t,lift_per_assy)
plt.xlabel('time [s]')
plt.ylabel('normal force per\n assembly [N]')
plt.grid()

plt.subplot(717)
plt.plot(t,gap)
plt.xlabel('time [s]')
plt.ylabel('magnet to I-beam\ngap [m]')
plt.grid()

plt.show()
