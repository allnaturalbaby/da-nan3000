#!/bin/bash

echo -e "GET /$1 HTTP/1.0\n" | nc 127.0.0.1 80