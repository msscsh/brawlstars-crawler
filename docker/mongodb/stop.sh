#!/bin/bash

docker stop  $(docker ps -q --filter name=mongo_bs_crawler_container)
docker container rm mongo_bs_crawler_container