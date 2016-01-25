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

plt.subplot(311)
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
plt.text(15,-550,'contour labels:\nmagnet to rail gap [m]\n- braking force\n-- normal force',fontsize=8)

plt.subplot(312)
for i in df['h'].unique():
  dfi = df[df['h']==i]
  dfi = dfi.sort(['v'])
  plt.plot(dfi['v'],dfi['q_max_rail_surf'],'-',label='gap = {}'.format(i))
  if not np.isnan(eb.q_max(100,i).max()):
    plt.text(100,eb.q_max(100,i).max(),str(i),fontsize=8,ha='center')
plt.ylabel('max rail surface heating [W/m^3]')
plt.xlabel('velocity [m/s]')
plt.grid()

plt.subplot(313)
for i in df['h'].unique():
  dfi = df[df['h']==i]
  dfi = dfi.sort(['v'])
  plt.plot(dfi['v'],dfi['H_y_mean'],'-',label='gap = {}'.format(i))
  if not np.isnan(eb.H_y_mean(50,i).max()):
    plt.text(50,eb.H_y_mean(50,i).max(),str(i),fontsize=8,ha='center')
  plt.plot(dfi['v'],dfi['H_y_max'],'-',label='gap = {}'.format(i))
  if not np.isnan(eb.H_y_max(75,i).max()):
    plt.text(75.0,eb.H_y_max(75,i).max(),str(i),fontsize=8,ha='center')
plt.ylabel('H [A/m]')
plt.xlabel('velocity [m/s]')

plt.grid()
plt.show()
