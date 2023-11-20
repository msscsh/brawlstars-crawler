#!/bin/bash

CRONEXEC="cd $BS_CRAWLER_HOME && python3 src/rest/battlelog/feeder.py 2QPVJ099C"
(crontab -l ; echo "*/13 * * * * $CRONEXEC") | crontab -

echo "OK"
exit 0