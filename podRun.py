from scipy.integrate import odeint
from scipy.special import gamma, airy
from numpy import arange

x_0 = 0 # pod initial position
v_0 = 0 # pod initial velocity

def pusherForce(t):
  f = 1000.0
  if t > 10:
    f = 0.0
  return f

def brakeForce(t):
  if t<20:
    return 0
  else:
    return 1000

def dragForce(v):
  return 0.5*frontal_area*c_d*v**2  

x = [x0, v_0]
def func(y, t):
    #need to figure out what goes here...
    return [t*y[1],y[0]]


x = arange(0, 30, 0.01)
t = x
ychk = airy(x)[0]
y = odeint(func, y0, t)


print ychk[:36:6]


print y[:36:6,1]




