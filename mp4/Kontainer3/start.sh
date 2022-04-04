#!/bin/bash

docker build -t webgren .
docker run -dit --name kontainer-3 -p 8080:80 webgren
