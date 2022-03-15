#!/bin/bash

AUXPID=$(ps aux | less | grep ./improved | head -1 | awk '{ print $2 }')
sudo kill -s KILL $AUXPID

JOBPID=$(jobs -p | awk '{ print $3 }')   
sudo kill -s KILL $JOBPID
