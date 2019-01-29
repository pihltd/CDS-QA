#!/bin/bash
usage() { echo "Usage: $0 [-t <testmode>] [-f <list file>]" 1>&2; exit 1; }

TESTMODE="False"

while getopts "f:t" args; do
  case "${args}" in
    f)
      FILELIST=${OPTARG}
      ;;
    t)
      TESTMODE="True"
      ;;
    *)
      usage
      ;;
  esac
done

if [ "${TESTMODE}" == "True" ] ; then
  declare -a FILES=(${DEMOFILE})
else
  mapfile -t FILES < ${FILELIST}
fi

for i in "${FILES[@]}" ; do
  echo "$i"
  filename=$(basename -- "$i")
  docker run \
  -it \
  --rm \
  -e AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID} \
  -e AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY} \
  --entrypoint samtools \
  cdsqa:samtools \
  view -H ${DEMOFILE} >> "${filename}.header.txt"
done
