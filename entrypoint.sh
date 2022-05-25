#!/bin/bash

set -e

if [ -z "$INPUT_FILE_NAME" ]; then
  echo '::error::Required file_name parameter'
  exit 1
fi

if [ -z "$INPUT_FILE_PATH" ]; then
  echo '::error::Required file_path parameter'
  exit 1
fi

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

python ./upload.py uploads -n $INPUT_FILE_NAME -p $INPUT_FILE_PATH -u $INPUT_UPLOAD_PATH -c $INPUT_CLIENT_ID -r $INPUT_REDIRECT_URI -s $INPUT_CLIENT_SECRET -t $INPUT_REFRESH_TOKEN
echo "python ./upload.py uploads -n $INPUT_FILE_NAME -p $INPUT_FILE_PATH -u $INPUT_UPLOAD_PATH -c $INPUT_CLIENT_ID -r $INPUT_REDIRECT_URI -s $INPUT_CLIENT_SECRET -t $INPUT_REFRESH_TOKEN"
echo "Commands ran successfully"
