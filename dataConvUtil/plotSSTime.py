import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('ssTime.csv')
df['d/l'] = df['v']*df['ss_time']/0.10795

plt.figure()

plt.subplot(211)
plt.plot(df['v'],df['ss_time'],'o')
plt.xlabel('v [m/s]')
plt.ylabel('time to reach steady state [s]')
plt.grid()

plt.subplot(212)
plt.plot(df['v'],df['d/l'],'o')
plt.xlabel('v [m/s]')
plt.ylabel('distance traveled / domain length')
plt.grid()

def y(x):
  return 0.147 * x

def y1(x):
  return 0.2 * x + 2

plt.plot([0,150],[y(0),y(150)],label = 'fit to load pts already simulated')
plt.plot([0,150],[y1(0),y1(150)],label = 'Recommended for future runs:\n d/l = 0.2*v + 2')
plt.legend(loc='upper left')

plt.show()

