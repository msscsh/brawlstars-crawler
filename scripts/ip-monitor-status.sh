#!/bin/bash

MONITOR_FOLDER=""
SPECIFIC_FILE="python-error.log"
while true; do

  EVENT=$(inotifywait -e create --format "%f" "$MONITOR_FOLDER")
  
  if [[ "$EVENT" == "$SPECIFIC_FILE" ]]; then
    rm $MONITOR_FOLDER'/'$SPECIFIC_FILE
    npm run keys
  fi
  
done
