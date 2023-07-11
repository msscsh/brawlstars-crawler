#!/bin/bash

# Brawl Stars API Key
echo $BSAPIKEY
# Club tag to be used
echo $CLUBTAG

# output file
OUTPUT_FILE="src/commons/files/club_data.json"

rm -f src/commons/files/club_data.json

# Makes GET request to API and saves output to output file
response=$(curl -s -o /dev/null -w "%{http_code}" "https://api.brawlstars.com/v1/clubs/%23${CLUBTAG}" -H "Authorization: Bearer $BSAPIKEY")
if [ "$response" -eq 200 ]; then
    curl -s "https://api.brawlstars.com/v1/clubs/%23${CLUBTAG}" \
    -H "Authorization: Bearer $BSAPIKEY" \
    -o "$OUTPUT_FILE"
    echo "API data was saved in $OUTPUT_FILE"
else
  echo "Request failed, check environment variables (status code $response)"
fi

