#!/bin/bash

rm -f src/commons/files/club_data.json
rm -f src/commons/files/master.json
rm -f src/commons/files/member_*_data.json

BSAPIKEY=$(jq -r '.BSAPIKEY' shell.json)

# output file
OUTPUT_FILE="src/commons/files/club_data.json"
# Makes GET request to API and saves output to output file
response=$(curl -s -o /dev/null -w "%{http_code}" "https://api.brawlstars.com/v1/clubs/%23${CLUBTAG}" -H "Authorization: Bearer $BSAPIKEY")
if [ "$response" -eq 200 ]; then
    curl -s "https://api.brawlstars.com/v1/clubs/%23${CLUBTAG}" \
    -H "Authorization: Bearer $BSAPIKEY" \
    -o "$OUTPUT_FILE"
    echo "CLUB data was saved in $OUTPUT_FILE"

    jq '.members = []' src/commons/files/club_data.json > src/commons/files/master.json

    for tag in $(jq -r '.members[].tag' src/commons/files/club_data.json); do

      OUTPUT_FILE="src/commons/files/member_${tag:1}_data.json"

      curl -s "https://api.brawlstars.com/v1/players/%23${tag:1}" \
      -H "Authorization: Bearer $BSAPIKEY" \
      -o "$OUTPUT_FILE"

      echo "Member file created in $OUTPUT_FILE"


      tmp_file=$(mktemp)  # Cria um arquivo temporário
      jq --argjson groupInfo "$(<$OUTPUT_FILE)" '.members += [$groupInfo]' src/commons/files/master.json > "$tmp_file"
      mv "$tmp_file" src/commons/files/master.json

      # jq --argjson groupInfo "$(<$OUTPUT_FILE)" '.members += [$groupInfo]' src/commons/files/master.json > src/commons/files/out.json

    done

    rm -f src/commons/files/club_data.json
    rm -f src/commons/files/member_*_data.json


else
  echo "Request failed, check environment variables (status code $response)"
fi

