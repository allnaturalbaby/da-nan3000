#!/bin/bash

docker build -t shelltestserver .
docker run -dit --name Kontainer-3 -p 8080:80 shelltestserver 
docker run -dit --name Kontainer-2 -p 8180:80 shelltestserver
