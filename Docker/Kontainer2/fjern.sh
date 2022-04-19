#!/bin/bash
docker stop kontainer-2
docker rmi -f restapi
echo "Fjernet kontainer2 og restapi(image)"
