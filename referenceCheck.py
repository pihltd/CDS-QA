#!/usr/bin/env python
#Script to check the MD5sum values for reference sequences against EBI

import argparse
import requests
import re
import pprint

def getMD5(headerfile, verbose):
  #Returns a list of all unique md5 values in a samtools header file
  md5list = []
  headerfile = headerfile.rstrip()
  if verbose:
    print(headerfile)
  with open(headerfile, 'r') as f:
    for line in f:
      if '@SQ' in line:
        list = line.split()
        for each in list:
          if 'M5' in each:
            md5 = re.sub('M5:','',each)
            if md5 not in md5list:
              md5list.append(md5)
  return md5list

def main (args):

  #Open log file
  logfile = open(args.outputfile,'w')
  baseurl = "https://www.ebi.ac.uk/ena/cram/sequence/"
  #https://www.ebi.ac.uk/ena/cram/swagger-ui.html#/The_GA4GH_Refget_reference_sequence_retrieval_API.
  #Read the list of header files
  headerfiless = open(args.inputfile,'r')
  for headerfile in headerfiless:
    logfile.write("Checking file " + headerfile)
    md5list = getMD5(headerfile, args.verbose)
    if args.verbose:
      pprint.pprint(md5list)
    for md5 in md5list:
      try:
        r = requests.get(baseurl + md5 + "/metadata")
        if args.verbose:
          print(r.url)
          print(r.status_code)
          pprint.pprint(r.json())
        if r.json()['metadata']['md5'] is None:
          logfile.write(("File\t%s\tMD5:\t%s\tMD5 value not found\n") % (headerfile, md5))
      except requests.exceptions.Timeout as exception:
        logfile.write(("File:\t%s\tMD5:\t%s\tTimeout error:\t%s\n") % (headerfile, md5,exception))
      except requests.exceptions.HTTPError as exception:
        logfile.write(("File:\t%s\tMD5:\t%s\tHTTPEerror:\t%s\n") % (headerfile, md5,exception))
  logfile.close()
  
if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("-v", "--verbose", action = "store_true", help = 'Enable verbose feedback.')
  parser.add_argument("-i", "--inputfile", required = True, help = "File with list of samtools headers output")
  parser.add_argument("-o", "--outputfile", required = True, help = "File for storing unique data")

  args = parser.parse_args()
  main(args)
