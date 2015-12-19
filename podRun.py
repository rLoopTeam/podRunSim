from scipy.integrate import odeint
from scipy.special import gamma, airy
from numpy import arange
y1_0 = 1.0 / 3**(2.0/3.0) / gamma(2.0/3.0)
y0_0 = -1.0 / 3**(1.0/3.0) / gamma(1.0/3.0)
y0 = [y0_0, y1_0]
def func(y, t):
    return [t*y[1],y[0]]


def gradient(y, t):
    return [[0,t], [1,0]]


x = arange(0, 4.0, 0.01)
t = x
ychk = airy(x)[0]
y = odeint(func, y0, t)
y2 = odeint(func, y0, t, Dfun=gradient)


print ychk[:36:6]


print y[:36:6,1]


print y2[:36:6,1]


