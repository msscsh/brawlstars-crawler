#!/bin/bash

# Remove existing files
rm -f src/commons/files/club_data.json
rm -f src/commons/files/master.json
rm -f src/commons/files/member_*_data.json

# Get BSAPIKEY from shell.json using jq
BSAPIKEY=$(jq -r '.BSAPIKEY' shell.json)

# Function to handle errors and exit with non-zero status code
handle_error() {
  echo "Error: $1"
  exit 1
}

# Output file
OUTPUT_FILE="src/commons/files/club_data.json"

# Make GET request to API and save output to output file
response=$(curl -s -o /dev/null -w "%{http_code}" "https://api.brawlstars.com/v1/clubs/%23${CLUBTAG}" -H "Authorization: Bearer $BSAPIKEY")
if [ "$response" -eq 200 ]; then
  curl -s "https://api.brawlstars.com/v1/clubs/%23${CLUBTAG}" \
  -H "Authorization: Bearer $BSAPIKEY" \
  -o "$OUTPUT_FILE" || handle_error "Failed to save CLUB data in $OUTPUT_FILE"

  echo "CLUB data was saved in $OUTPUT_FILE"

  # Create the master.json file with empty 'members' array
  jq '.members = []' "$OUTPUT_FILE" > src/commons/files/master.json || handle_error "Failed to create master.json"

  # Loop through members and save individual files
  for tag in $(jq -r '.members[].tag' "$OUTPUT_FILE"); do
    OUTPUT_FILE="src/commons/files/member_${tag:1}_data.json"

    curl -s "https://api.brawlstars.com/v1/players/%23${tag:1}" \
    -H "Authorization: Bearer $BSAPIKEY" \
    -o "$OUTPUT_FILE" || handle_error "Failed to save member file in $OUTPUT_FILE"

    echo "Member file created in $OUTPUT_FILE"

    # Add member data to the master.json
    tmp_file=$(mktemp)  # Create a temporary file
    jq --argjson groupInfo "$(<$OUTPUT_FILE)" '.members += [$groupInfo]' src/commons/files/master.json > "$tmp_file" || handle_error "Failed to update master.json"
    mv "$tmp_file" src/commons/files/master.json || handle_error "Failed to update master.json"
  done

  # Clean up
  rm -f src/commons/files/club_data.json
  rm -f src/commons/files/member_*_data.json

else
  handle_error "Request failed, check environment variables (status code $response)"
fi
