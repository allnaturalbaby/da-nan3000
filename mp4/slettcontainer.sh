#!/bin/bash
echo "Start!"
for ID in $(sudo docker ps -aqf "name=$")
do
    docker kill "${ID}"
    docker rm -f "${ID}" 
    echo "exterminated" 
done
echo "exterminated"
