#!/bin/bash

#docker build -t shelltestserver .
#docker run -dit --name Kontainer-3 -p 8080:80 shelltestserver 
#docker run -dit --name Kontainer-2 -p 8180:80 shelltestserver


docker build -t webgren .
docker run -dt --rm --name kontainer-3 -p 8080:80 --cpus=0.5 --cap-drop ALL webgren

docker build -t restapi .
docker run -dt --rm --name kontainer-2 -p 8180:80 --cpus=0.5 --cap-drop CHOWN restapi