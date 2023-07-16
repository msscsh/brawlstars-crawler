#!/bin/bash

rm -f cypress.env.json

env_vars='{
  "BS_EMAIL": "'"${BS_EMAIL}"'",
  "BS_PASSWORD": "'"${BS_PASSWORD}"'",
  "EXTERNAL_IP": "'"${EXTERNAL_IP}"'"
}'

echo "$env_vars" > cypress.env.json
echo "File cypress.env.json generated with success."