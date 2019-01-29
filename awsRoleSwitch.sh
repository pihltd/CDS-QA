#!/bin/bash

usage(){ echo "Usage: $0 [-a <arn identifier>] [-n <session name>]" 1>&2; exit 1; }

while getopts a:n: args; do
  case "${args}" in
    a)
      ARN=${OPTARG}
      ;;
    n)
     NAME=${OPTARG}
     ;;
   *)
     usage
     ;;
  esac
done

if [ -z "$ARN" ]
then
  usage
fi
if [ -z "$NAME" ]
then
  usage
fi
#aws sts assume-role --role-arn "${ARN}" --role-session-name "${NAME}" | jq '.Credentials.AccessKeyId'
#aws sts assume-role --role-arn "${ARN}" --role-session-name "${NAME}" | jq '. | {id: .Credentials.AccessKeyId, key: .Credentials.SecretAccessKey, token: .Credentials.SessionToken}'
JSON="$(aws sts assume-role --role-arn "${ARN}" --role-session-name "${NAME}")"
ID=($(jq -r '.Credentials.AccessKeyId' <<< "$JSON"))
KEY=($(jq -r '.Credentials.SecretAccessKey' <<< "$JSON"))
TOKEN=($(jq -r '.Credentials.SessionToken' <<< "$JSON"))
export AWS_ACCESS_KEY="$ID"
export AWS_SECRET_ACCESS_KEY="$KEY"
export AWS_SESSION_TOKEN="$TOKEN"

