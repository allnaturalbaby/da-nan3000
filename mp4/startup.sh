#!/bin/bash

docker build -t shelltestserver .
docker run -dit --userns=host --name Kontainer-3 -p 8080:80 shelltestserver 
docker run --userns=host -dit --name Kontainer-2 -p 8180:80 shelltestserver
