#!/bin/bash
PID=$(ps aux | less | grep ./improved | head -1 | awk '{ print $2 }')

kill $PID