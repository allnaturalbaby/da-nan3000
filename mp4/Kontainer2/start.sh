#!/bin/bash

docker build -t restapi . 
docker run -dit --name kontainer-2 -p 8180:80 restapi
