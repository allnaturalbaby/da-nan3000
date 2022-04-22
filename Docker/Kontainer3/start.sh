#!/bin/bash

docker build -t webgren .
docker run -dt --rm --name kontainer-3 -p 8080:80 --cpus=0.5 --cap-drop ALL webgren
