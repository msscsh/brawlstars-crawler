#!/bin/bash

echo "Trying to stop possible existing docker machine"
docker stop  $(docker ps -q --filter name=mongo_bs_crawler_container)

echo "Trying to remove possible existing docker container"
docker rm  $(docker container ls -q --filter name=mongo_bs_crawler_container -a)