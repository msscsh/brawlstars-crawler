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

if [ -z "$AUTO_GIT_USERNAME" ]; then
  echo "Must create AUTO_GIT_USERNAME enviroment variable."
  exit 1
else
  echo "AUTO_GIT_USERNAME: $AUTO_GIT_USERNAME"
fi
CRONEXEC="cd $BS_CRAWLER_HOME && sh scripts/create-ranking-html.sh $SITE_APP_HOME $AUTO_GIT_USERNAME $AUTO_GIT_EMAIL $GIT_USERNAME $GIT_EMAIL"
(crontab -l ; echo "5,35 * * * * $CRONEXEC") | crontab -

echo "OK"
exit 0
