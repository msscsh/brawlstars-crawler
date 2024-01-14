#!/bin/bash
if [ -z "$MONGO_BACKUP_HOME" ]; then
  echo "Must create MONGO_BACKUP_HOME enviroment variable."
  exit 1
else
  echo "MONGO_BACKUP_HOME: $MONGO_BACKUP_HOME"
fi

CRONEXEC="mongodump --host localhost --port 27017 --db brawlstars_crawler --out $MONGO_BACKUP_HOME"
(crontab -l ; echo "8 0 * * * $CRONEXEC") | crontab -

echo "OK"
exit 0