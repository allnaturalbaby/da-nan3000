FROM httpd:alpine

RUN apk update && apk upgrade && apk add nano && apk add --no-cache bash

COPY ./my-httpd.conf /usr/local/apache2/conf/httpd.conf