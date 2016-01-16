import argparse
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import EddyBrake

parser = argparse.ArgumentParser()
parser.add_argument('infile')
args = parser.parse_args()

df = pd.read_csv(args.infile)
eb = EddyBrake.EddyBrake(args.infile)

plt.figure()

plt.subplot(211)
for i in df['h'].unique():
  dfi = df[df['h']==i]
  dfi = dfi.sort(['v'])
  plt.plot(dfi['v'],dfi['F_lift'],'--',label='gap = {}'.format(i))
  plt.plot(dfi['v'],dfi['F_drag'],'-',label='gap = {}'.format(i))
  if not np.isnan(eb.f_drag(5,i).max()):
    plt.text(5.0,eb.f_drag(5,i).max(),str(i),fontsize=8,ha='center')
  if not np.isnan(eb.f_lift(25,i).max()):
    plt.text(25.0,eb.f_lift(25,i).max(),str(i),fontsize=8,ha='center')
plt.xlabel('velocity [m/s]')
plt.ylabel('force [N]')
plt.grid()
plt.text(15,-750,'contour labels:\nmagnet to rail gap [m]\n- braking force\n-- normal force',fontsize=8)

plt.subplot(212)
for i in df['h'].unique():
  dfi = df[df['h']==i]
  dfi = dfi.sort(['v'])
  plt.plot(dfi['v'],dfi['q_max_rail_surf'],'-',label='gap = {}'.format(i))
plt.ylabel('max rail surface heating [W/m^3]')
plt.xlabel('velocity [m/s]')
plt.grid()

plt.show()
