FROM httpd:alpine

RUN apk update && apk upgrade && apk add nano && apk add sqlite && apk add --no-cache bash

#WORKDIR dikt
COPY ./index.html /usr/local/apache2/htdocs
COPY ./cgi-bin/* /usr/local/apache2/cgi-bin
COPY ./my-httpd.conf /usr/local/apache2/conf/httpd.conf

#EXPOSE 80

#STOPSIGNAL SIGWINCH
 
RUN chmod 755 /usr/local/apache2/cgi-bin/Webgren.cgi
CMD ["httpd","-D","FOREGROUND"] 

