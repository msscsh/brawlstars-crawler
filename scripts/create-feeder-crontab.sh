#!/bin/bash
if [ -z "$BS_CRAWLER_HOME" ]; then
  echo "Must create BS_CRAWLER_HOME enviroment variable."
  exit 1
else
  echo "BS_CRAWLER_HOME: $BS_CRAWLER_HOME"
fi

CRONEXEC="cd $BS_CRAWLER_HOME && python3 src/battlelog/feeder.py 2QPVJ099C"
(crontab -l ; echo "*/13 * * * * $CRONEXEC") | crontab -

echo "OK"
exit 0
