#!/bin/bash


NAME_VOLUME_MONGO_DOCKER=bs_crawler_data
NAME_CONTAINER_MONGO_DOCKER=mongo_bs_crawler_container

mkdir -p $BS_CRAWLER_HOME/docker/mongodb/data

if docker volume ls -q -f name=$NAME_VOLUME_MONGO_DOCKER | grep -q $NAME_VOLUME_MONGO_DOCKER; then
    echo "Volume already exists."
else
	docker volume create -d local -o type=none -o o=bind -o device=$PWD/docker/mongodb/data $NAME_VOLUME_MONGO_DOCKER
    echo "Volume created."
fi

sh $BS_CRAWLER_HOME/docker/mongodb/stop.sh

docker run -d -p 27017:27017 --name $NAME_CONTAINER_MONGO_DOCKER -v $NAME_VOLUME_MONGO_DOCKER:/data/db mongo

