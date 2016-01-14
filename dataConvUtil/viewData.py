import pandas as pd
import matplotlib.pyplot as plt
import re

#dfData = pd.read_csv('DataTable1.csv')
#dfForce = pd.read_csv('ForceTable.csv')

def convertTimeUnits(df):
  # check if time units need conversion
  p=re.compile(r'Time \[(.*)\]')
  columns = []
  for i in df.columns:
    match = p.match(i)
    if match:
      columns.append('Time [s]')
      unit = match.expand(r'\1')
      if unit == 'ms':
        df[i] = df[i]/1000.
    else:
      columns.append(i)
  df.columns = columns
  return df

def readInAndGlobTogether(filelist):

  dfs = []
  for i in filelist:
    dfi = pd.read_csv(i)
    dfi = convertTimeUnits(dfi)
    dfs.append(dfi)

  df = dfs.pop()
  for i in dfs:
    df = pd.merge(df,i,how='outer',on='Time [s]')

  return df

def identifyVariations(df):
  """
  df is a globbed df with v and gap messily in columns
  """

  velPattern = re.compile(r'v=\'([0-9]*\.*[0-9]*)m_per_sec\'')
  gapPattern = re.compile(r'gap=\'([0-9]*\.*[0-9]*)mm\'')

  columns = 0
  missing = 0

  loadPoint = []
  #gap = []
  #velocity = []

  for i in df.columns:
    columns += 1
    gapMatch = gapPattern.search(i)
    velMatch = velPattern.search(i)
    if not (gapMatch and velMatch):
      missing += 1
      #print('No variation data in column: {}'.format(i))
    else:
      h = float(gapMatch.expand(r'\1'))
      v = float(velMatch.expand(r'\1'))
      loadPoint.append((v,h))

  print('identified {} of {} columns'.format(columns-missing,columns))
  dfV = pd.DataFrame({'variation':loadPoint})

  variations = dfV['variation'].unique()

  v = []
  h = []
  for i in variations:
    v.append(i[0])
    h.append(i[1])
  
  dfOut = pd.DataFrame({'velocity':v,'gap':h})
  return dfOut

def plotLoadPointCoverage(dfV):

  plt.scatter(dfV['velocity'],dfV['gap'])
  plt.ylabel('gap [mm]')
  plt.xlabel('velocity [m/s]')
  plt.grid()
  plt.show()

def filterGlobbedByLoadPoint(raw,v,h):

  columns = ['Time [s]']
  velPattern = re.compile(r'v=\'([0-9]*\.*[0-9]*)m_per_sec\'')
  gapPattern = re.compile(r'gap=\'([0-9]*\.*[0-9]*)mm\'')

  for i in raw.columns:
    gapMatch = gapPattern.search(i)
    velMatch = velPattern.search(i)
    if not (gapMatch and velMatch):
      #print('No variation data in column: {}'.format(i))
      continue
    else:
      hCol = float(gapMatch.expand(r'\1'))
      vCol =float(velMatch.expand(r'\1'))
      if ((v == vCol) and (h == hCol)):
        columns.append(i)

  sparse = raw[columns]
  
  twoColDfs = []
  for col in sparse.columns:
    if col == 'Time [s]':
      continue
    twoColI = sparse[['Time [s]',col]]
    filled = twoColI[twoColI[col].isnull() == False]
    twoColDfs.append(filled)

  dfOut = twoColDfs.pop()
  for i in twoColDfs:
    dfOut = pd.merge(dfOut,i,how='outer',on='Time [s]')

  dfOut['v'] = v
  dfOut['h'] = h

  #convert units in brackets
  unitsToConvert = {
    'mNewton':(0.001,'newton'),
    'kNewton':(1000.0,'newton')
    }
  unitPattern = re.compile(r'(.*\[)(.*)(\].*)')
  for col in dfOut.columns:
    match = unitPattern.search(col)
    if match:
      unit = match.expand(r'\2')
      #print(unit)
      if unit in unitsToConvert.keys():
        newName = match.expand(r'\1{}\3'.format(unitsToConvert[unit][1]))
        dfOut[newName] = dfOut[col] * unitsToConvert[unit][0]
        dfOut = dfOut.drop(col,1)
        #print('non-conforming unit!')


  #get rid of units in column names
  p = re.compile(r'(.*)( \[)')
  newCols = []
  for col in dfOut.columns: 

    if col == 'Time [s]':
      newCols.append(col)
      continue

    match = p.match(col)

    if not match:
      newCols.append(col)
      continue

    newCols.append(match.expand(r'\1'))

  dfOut.columns = newCols

  #rename columns based on regex
  columnKey = [
               (re.compile(r'q_rail_surf_mean'),'q_rail_surf_mean'),
               (re.compile(r'q_max_rail_surf'),'q_max_rail_surf'),
               (re.compile(r'H_y_max'),'H_y_max'),
               (re.compile(r'H_y_mean'),'H_y_mean')
              ]
  columns = []
  for col in dfOut.columns:
    rename = False
    for p,name in columnKey:
      match = p.search(col)
      if match:
        columns.append(name)
        rename = True
        break
    if rename==False:
      columns.append(col)

  dfOut.columns = columns

  # replacement operations on rows
  unitsToConvert = [
    ('Force.Force_x',-1.0,'F_drag'),
    ('Force.Force_y',1.0,'F_lift'),
    ('h',0.001,'h')
    ]
  for oldName,factor,newName in unitsToConvert:
    dfOut[newName] = dfOut[oldName] * factor
    if not (oldName == newName):
      dfOut = dfOut.drop(oldName,1)

  return dfOut
  
def splitGlobbed(globbedDf):
  dfV = identifyVariations(globbedDf)
  dfs = []
  for i in range(dfV.shape[0]):
    var = dfV.iloc[i]
    dfs.append(filterGlobbedByLoadPoint(globbedDf,var['velocity'],var['gap']))
  return dfs

def flatten(globbedDf):
  dfs = splitGlobbed(globbedDf)

  df = pd.concat(dfs)
  return df

def getSS(dff):
  dfs = []
  for v in dff['v'].unique():
    for h in dff['h'].unique():
      dfi = dff[(dff['v']==v)&(dff['h']==h)]
      tMax = dfi['Time [s]'].max()
      dfi = dfi[dfi['Time [s]']==tMax]
      dfi = dfi.drop('Time [s]',1)
      dfs.append(dfi)

  df = pd.concat(dfs)
  return df

# plot all vs time
#  Force vs time
#  H vs time
#  q vs time

# plot pork chop plot

# export eddyBrakeData.csv
