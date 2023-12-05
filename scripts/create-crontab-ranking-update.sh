#!/bin/bash
if [ -z "$BS_CRAWLER_HOME" ]; then
  echo "Must create BS_CRAWLER_HOME enviroment variable."
  exit 1
else
  echo "BS_CRAWLER_HOME: $BS_CRAWLER_HOME"
fi

if [ -z "$SITE_APP_HOME" ]; then
  echo "Must create SITE_APP_HOME enviroment variable."
  exit 1
else
  echo "SITE_APP_HOME: $SITE_APP_HOME"
fi

CRONEXEC="cd $BS_CRAWLER_HOME && sh scripts/create-ranking-html.sh $SITE_APP_HOME"
(crontab -l ; echo "5,35 * * * * $CRONEXEC") | crontab -

echo "OK"
exit 0
