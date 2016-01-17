import argparse

class TrajectoryPlanner():

  def __init__(self,inputParameters):

    self.breakingCurves = {} 

    for i in inputParameters['breakingCurves']:
      try:
        self.breakingCurves[i] = pd.read_csv(i)
      except:
        print('failed to load breaking curve: {}'.format(i))

    self.xFinal = inputParameters['xFinal']
    self.vMax = inputParameters['vMax']
    self.xMaxAccel = inputParameters['vMax']
    self.accel = inputParameters['accel']

  def calulate(accel,vMax,xMaxAccel,xFinal,breakCurve):
    message = ''

    d_a = 0.5*vMax**2/accel
    t_1 = vMax/accel

    # will the accel profile fit in xMaxAccel?
    if d_a > xMaxAccel:
      message += 'accel profile displacement is greater than xMaxAccel\n'

    d_d = None
    # can the decel profile handle v_max?
    if breakCurve['velocity [m/s]'].max()<vMax:
      message += 'decel curve max velocity is less than requested vMax\n'


    d_d = 

    # how much time at steady speed is needed to get to xFinal?

    return t1,t2,t3

parser = argparse.ArgumentParser()
parser.add_argument('-b','--brakeProfile',help="csv file with brake velocity profile.  Must contain the columns ")
parser.add_argument('-i','infile','input file')




dt = 0.01
while t<1000:
  
