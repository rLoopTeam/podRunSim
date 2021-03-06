import numpy as np
import matplotlib.pyplot as plt
from viewData import *
import pdb
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('input',nargs='+')
args = parser.parse_args()

#df = readInAndGlobTogether(['DataTable1.csv','ForceTable.csv','force.csv','demag.csv'])
#df = readInAndGlobTogether(['force.csv','demag.csv'])
#df = readInAndGlobTogether(['force7.csv','dmag7.csv'])
#df = readInAndGlobTogether(['force8.csv','demag8.csv'])
df = readInAndGlobTogether(args.input)
dfv = identifyVariations(df)
#dfv['h'] = dfv['gap']*0.001
dff = flatten(df)

fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_title('variations')
line, = ax.plot(dfv['velocity'], dfv['gap'], 'o', picker=5)  # 5 points tolerance

plt.ylabel('gap [mm]')
plt.xlabel('velocity [m/s]')
plt.grid()

def onpick(event):

    if event.artist!=line: return True

    N = len(event.ind)
    if not N: return True

    #print('x:{} y:{}'.format(event.mouseevent.xdata,event.mouseevent.ydata))

    x = event.mouseevent.xdata
    y = event.mouseevent.ydata

    dfvCopy = dfv.copy()
    dfvCopy['dx'] = abs(dfv['velocity'] - x)
    dfvCopy['dy'] = abs(dfv['gap']      - y)

    min_dx = dfvCopy['dx'].min()
    min_dy = dfvCopy['dy'].min()

    v = dfvCopy[dfvCopy['dx'] == min_dx]['velocity'].unique()
    h = dfvCopy[dfvCopy['dy'] == min_dy]['gap'].unique()
    if (len(h)!=1) or (len(v)!=1):
      print('Please click more precisely, clumsy clod!') 
      return True

    v = v[0]
    h = h[0]

    vTol = 0.001
    hTol = 0.00001
    vMask = (dff['v'] < (v + vTol)) & (dff['v'] > (v - vTol))
    hMask = (dff['h'] < (h/1000. + hTol)) & (dff['h'] > (h/1000. - hTol))
    dff_slice = dff[vMask&hMask]

    figi = plt.figure()
    plt.subplot(311)

    plt.title('v = {} m/s, h = {} mm'.format(v,h))
    plt.plot(dff_slice['Time [s]'],dff_slice['F_drag'],'o',label='drag')
    plt.plot(dff_slice['Time [s]'],dff_slice['F_lift'],'o',label='lift')
    plt.xlabel('Time [s]')
    plt.ylabel('Force [N]')
    plt.legend()
    plt.grid()

    plt.subplot(312)
    plt.plot(dff_slice['Time [s]'],dff_slice['H_y_mean'],'o')
    plt.plot(dff_slice['Time [s]'],dff_slice['H_y_max'],'o')
    plt.xlabel('Time [s]')
    plt.ylabel('H [A/m]')
    plt.grid()

    #pdb.set_trace()
    plt.subplot(313)
    plt.plot(dff_slice['Time [s]'],dff_slice['q_max_rail_surf'],'o')
    plt.plot(dff_slice['Time [s]'],dff_slice['q_rail_surf_mean'],'o')
    plt.xlabel('Time [s]')
    plt.ylabel('q [W/m^3]')
    plt.grid()

    #plt.plot([1,2,3],[4,5,6])
    figi.show()
    return True

fig.canvas.mpl_connect('pick_event', onpick)

plt.show()
