#!/bin/bash

EXTERNAL_IP=curl -sS https://api.ipify.org

if [ -z "$BS_EMAIL" ] || [ -z "$BS_PASSWORD" ] || [ -z "$EXTERNAL_IP" ]; then
  echo "Error: Environment variables BS_EMAIL, BS_PASSWORD and EXTERNAL_IP must be defined."
  exit 1
fi

rm -f cypress.env.json

env_vars='{
  "BS_EMAIL": "'"${BS_EMAIL}"'",
  "BS_PASSWORD": "'"${BS_PASSWORD}"'",
  "EXTERNAL_IP": "'"${EXTERNAL_IP}"'"
}'

if ! echo "$env_vars" > cypress.env.json; then
  echo "Error: fail in cypress.env.json file creation."
  exit 1
fi

echo "File cypress.env.json generated with success."
exit 0
