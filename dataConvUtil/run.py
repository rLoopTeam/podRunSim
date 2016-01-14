from viewData import *

#df = readInAndGlobTogether(['DataTable1.csv','ForceTable.csv','demag.csv','force.csv'])
df = readInAndGlobTogether(['demag.csv','force.csv'])
#dfv = identifyVariations(df)
#plotLoadPointCoverage(dfv)
#dfs = splitGlobbed(df)
#n_fifteens = 0
#fif = []
#for i in dfs:
#  if len(i.columns) == 15:
#    n_fifteens += 1
#    fif.append(i)

#print(n_fifteens)
dff = flatten(df)

dfss = getSS(dff)
