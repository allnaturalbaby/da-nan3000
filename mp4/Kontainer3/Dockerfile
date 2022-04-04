FROM httpd:alpine

RUN apk update && apk upgrade && apk add nano && apk add sqlite

WORKDIR dikt
COPY ./index.html /usr/local/apache2/htdocs
COPY ./Webgren.cgi /usr/local/apache2/cgi-bin
COPY ./my-httpd.conf /usr/local/apache2/conf/httpd.conf

EXPOSE 80

STOPSIGNAL SIGWINCH
 
RUN chmod 755 /usr/local/apache2/cgi-bin/Webgren.cgi
RUN apk add --no-cache bash
CMD ["httpd","-D","FOREGROUND"] 
CMD httpd-foreground -c "LoadModule cgid_module modules/mod_cgid.so"
