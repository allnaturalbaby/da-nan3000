FROM httpd:alpine

RUN apk update && apk upgrade && apk add bash && apk add nano

COPY ./index.html /usr/local/apache2/htdocs
#COPY /usr/lib/cgi-bin/* /usr/lib/cgi-bin

EXPOSE 80

STOPSIGNAL SIGWINCH

RUN apk add --no-cache bash
CMD ["httpd","-D","FOREGROUND"] 
