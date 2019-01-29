#!/usr/bin/env python

import pandas as pd
import numpy as np
import pprint
import argparse
import os
import sys
import datetime

def main(args):
  fulldf = pd.read_csv(args.inputfile, sep = '\t', header = 0)

  #Create an index of the number of unique values in each column
  unidex = fulldf.apply(lambda x: x.nunique())
  if args.verbose:
    pprint.pprint(unidex.sort_values(ascending=False))
  #Sort the columns in descending order by the number of unqiue values in each column
  cols = unidex.sort_values(ascending=False).index
  if args.verbose:
    for col in cols:
      print(col)
  #Reorder the columns
  ordereddf = fulldf[cols]
  #This would delete any columns that only have a single value
  #ordereddf = fulldf.drop(unidex[uniques==1].index,axis=1)

  ordereddf.to_csv(args.outputfile, sep='\t', encoding='utf-8')

if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("-v", "--verbose", action = "store_true", help = 'Enable verbose feedback.')
  parser.add_argument("-i", "--inputfile", required = True, help = "Input tab delimited file")
  parser.add_argument("-o", "--outputfile", required = True, help = "File for storing unique data")

  args = parser.parse_args()
  main(args)
