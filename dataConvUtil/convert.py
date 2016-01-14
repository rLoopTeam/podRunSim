from viewData import *

df = readInAndGlobTogether(['demag.csv','force.csv'])
dff = flatten(df)

conversions = {'F_lift':('Force.Force_x',1.0)}

cols = dff.columns
newCols = []

for i in cols:
  if i == 'Force.Force_y':
    newCols.append('F_lift')
    continue
  if i == 'Force.Force_x':
    newCols.append('F_drag')
    dff['Force.Force_x'] = - dff['Force.Force_x'] 
    continue
  newCols.append(i)

dff.columns = newCols

dff.to_csv('eddyBrakeData.csv') 
