#!/bin/bash

if docker volume ls -q -f name=bs_crawler_data | grep -q bs_crawler_data; then
    echo "Volume already exists."
else
	docker volume create -d local -o type=none -o o=bind -o device=$PWD/docker/mongodb/data bs_crawler_data
    echo "Volume created."
fi

sh $BS_CRAWLER_HOME/docker/mongodb/stop.sh

docker run -d -p 27017:27017 --name mongo_bs_crawler_container -v bs_crawler_data:/data/db mongo

