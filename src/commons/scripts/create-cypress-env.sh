#!/bin/bash

env_vars='{
  "BS_EMAIL": "'"${BS_EMAIL}"'",
  "BS_PASSWORD": "'"${BS_PASSWORD}"'"
}'

echo "$env_vars" > cypress.env.json
echo "File cypress.env.json generated with success."
