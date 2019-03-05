#!/usr/bin/env python
#Script to check the MD5sum values for reference sequences against EBI

import argparse
import requests
import re
import pprint

def getMD5(headerfile, md5list, verbose):
  #Returns a dictionary  of all unique md5 values in a samtools header file and the files they are found in
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
            if md5  in md5list.keys():
                md5list[md5] = md5list[md5].append(headerfile)
            else:
                md5list[md5] = [headerfile]
  return md5list

def main (args):

  #Open log file
  logfile = open(args.outputfile,'w')
  baseurl = "https://www.ebi.ac.uk/ena/cram/sequence/"
  #https://www.ebi.ac.uk/ena/cram/swagger-ui.html#/The_GA4GH_Refget_reference_sequence_retrieval_API.
  #Read the list of header files
  headerfiles = open(args.inputfile,'r')
  md5list = {}
  #For each headerfile, get a list of overall unique md5 values
  for headerfile in headerfiles:
    logfile.write("Checking file " + headerfile)
    md5list = getMD5(headerfile, md5list, args.verbose)
  #Check each md5 against the ENA database and log only failures
  for (md5, filelist) in md5list.items():
    try:
      r = requests.get(baseurl + md5 + "/metadata")
      if args.verbose:
        print(r.url)
        print(r.status_code)
        pprint.pprint(r.json())
      if r.json()['metadata']['md5'] is None:
        logfile.writ(("MD5:\t%s\tMD5 Error:\tNot found\tFiles:\t%s\t") % (md5, ' '.join(filelist)))
    except requests.exceptions.Timeout as exception:
      logfile.write(("MD5:\t%s\tTimeout error:\t%s\tFiles:\t%s\n") % (md5,exception, ' '.join(filelist)))
    except requests.exceptions.HTTPError as exception:
      logfile.write(("MD5:\t%s\tHTTPError:\t%s\tFiles:\t%s\n") % (md5,exception, ' '.join(filelist)))
  logfile.close()

if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("-v", "--verbose", action = "store_true", help = 'Enable verbose feedback.')
  parser.add_argument("-i", "--inputfile", required = True, help = "File with list of samtools headers output")
  parser.add_argument("-o", "--outputfile", required = True, help = "File for storing unique data")

  args = parser.parse_args()
  main(args)
