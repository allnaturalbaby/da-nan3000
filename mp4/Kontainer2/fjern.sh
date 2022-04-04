#!/bin/bash
docker rm -f kontainer-2
docker rmi -f restapi
echo "Fjernet kontainer2 og restapi(image)"
