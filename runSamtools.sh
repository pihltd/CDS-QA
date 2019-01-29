#!/bin/bash
usage() { echo "Usage: $0 [-t <testmode>] [-f <list file>] [-h samtools header] [-s samtols stats] [-q samtools fastq] [-r <results bucket location>]" 1>&2; exit 1; }

TESTMODE="False"
SAMCMD="view -H"
OUTPUT="header"
SUFFIX="txt"
BUCKET="na"

while getopts "f:thsqr:" args; do
  case "${args}" in
    f)
      FILELIST=${OPTARG}
      ;;
    t)
      TESTMODE="True"
      ;;
    h)
      SAMCMD="view -H"
      OUTPUT="header"
      SUFFIX="txt"
      ;;
    s)
      SAMCMD="stats"
      OUTPUT="stats"
      SUFFIX="txt"
      ;;
    q)
      SAMCMD="fastq"
      OUTPUT="fastq"
      SUFFIX="fastq"
      ;;
    r)
      BUCKET=${OPTARG}
      ;;
    *)
      usage
      ;;
  esac
done

if [ "${BUCKET}" = "na" ]; then
  usage
fi

if [ "${TESTMODE}" == "True" ] ; then
  declare -a FILES=(${DEMOFILE})
else
  mapfile -t FILES < ${FILELIST}
fi

for i in "${FILES[@]}" ; do
  echo "$i"
  filename=$(basename -- "$i")
  samtools ${SAMCMD} ${i} >> "${filename}.${OUTPUT}.${SUFFIX}"
  aws s3 mv "${filename}.${OUTPUT}.${SUFFIX}" "${BUCKET}${filename}.${OUTPUT}.${SUFFIX}" --profile gecco
done
