import argparse
from viewData import *

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", help="input files",nargs='+')
parser.add_argument("-o","--output",help="output file")
args = parser.parse_args()

df = readInAndGlobTogether(args.input)
dff = flatten(df)
dfss = getSS(dff)
dfss.to_csv(args.output)
