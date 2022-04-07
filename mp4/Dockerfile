FROM httpd:alpine

RUN apk update && apk upgrade && apk add nano && apk add sqlite

WORKDIR dikt
COPY ./index.html /usr/local/apache2/htdocs
COPY ./diktbase.db /usr/local/apache2/dikt
COPY ./cgi-bin/* /usr/local/apache2/cgi-bin
COPY ./my-httpd.conf /usr/local/apache2/conf/httpd.conf
COPY ./diktbase.xsl /usr/local/apache2/htdocs

EXPOSE 80

STOPSIGNAL SIGWINCH

RUN chmod -R 777 /usr/local/apache2/dikt/ 
RUN chmod 755 /usr/local/apache2/cgi-bin/diktbase.cgi
RUN apk add --no-cache bash
RUN apk add libxml2-utils
CMD ["httpd","-D","FOREGROUND"] 
CMD httpd-foreground -c "LoadModule cgid_module modules/mod_cgid.so"
