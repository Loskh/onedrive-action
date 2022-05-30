#!/bin/bash

set -e

if [ -z "$INPUT_UPLOAD_PATH" ]; then
  echo '::error::Required upload_path parameter'
  exit 1
fi

if [ -z "$INPUT_CLIENT_ID" ]; then
  echo '::error::Required client_id parameter'
  exit 1
fi

if [ -z "$INPUT_REDIRECT_URI" ]; then
  echo '::error::Required redirect_uri parameter'
  exit 1
fi

if [ -z "$INPUT_CLIENT_SECRET" ]; then
  echo '::error::Required client_secret parameter'
  exit 1
fi

if [ -z "$INPUT_REFRESH_TOKEN" ]; then
  echo '::error::Required refresh_token parameter'
  exit 1
fi


if [ -n "$INPUT_FILES" ];then
  IFS="&&"
  arrARGS=($INPUT_FILES)

  for each in ${arrARGS[@]}
  do
    unset IFS
    each=$(echo ${each} | xargs)
    if [ -n "$each" ]; then
    python /upload.py file ${each} -u $INPUT_UPLOAD_PATH -c $INPUT_CLIENT_ID -r $INPUT_REDIRECT_URI -s $INPUT_CLIENT_SECRET -t $INPUT_REFRESH_TOKEN
    echo "Running command: upload ${each}"
    fi
  done
fi


if [ -d "$INPUT_FOLDER" ];then
  # path = `realpath $INPUT_FOLDER`
  python /upload.py folder ${INPUT_FOLDER} -u $INPUT_UPLOAD_PATH -c $INPUT_CLIENT_ID -r $INPUT_REDIRECT_URI -s $INPUT_CLIENT_SECRET -t $INPUT_REFRESH_TOKEN
  echo "Running command: upload ${path}"
fi


echo "Commands ran successfully"