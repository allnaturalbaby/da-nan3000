#!/bin/bash

docker build -t restapi .
docker run -dt --rm --name kontainer-2 -p 8180:80 --cpus=0.5 --cap-drop CHOWN restapi
