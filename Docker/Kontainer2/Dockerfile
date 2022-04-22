FROM mp4docker

RUN apk add sqlite && apk add libxml2-utils && apk add util-linux

COPY ./index.html /usr/local/apache2/htdocs
COPY ./diktbase.xsl /usr/local/apache2/htdocs
COPY ./diktbase.db /usr/local/apache2/diktbase.db
COPY ./cgi-bin/* /usr/local/apache2/cgi-bin/

RUN chmod -R 777 /usr/local/apache2/diktbase.db 
RUN chmod 755 /usr/local/apache2/cgi-bin/diktbase.cgi

CMD ["httpd","-D","FOREGROUND"] 
