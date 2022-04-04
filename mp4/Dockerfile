FROM httpd:alpine

RUN apk update && apk upgrade && apk add nano && apk add sqlite && apk add --no-cache bash

#WORKDIR dikt
COPY ./index.html /usr/local/apache2/htdocs
COPY ./diktbase.db /usr/local/apache2/diktbase.db
COPY ./cgi-bin/* /usr/local/apache2/cgi-bin/
COPY ./my-httpd.conf /usr/local/apache2/conf/httpd.conf

#EXPOSE 80

#STOPSIGNAL SIGWINCH

RUN chmod -R 777 /usr/local/apache2/diktbase.db 
RUN chmod 755 /usr/local/apache2/cgi-bin/diktbase.cgi
RUN chmod 755 /usr/local/apache2/cgi-bin/test.cgi
#RUN chcon -t httpd_sys_content_t /usr/local/apache2/cgi-bin/test.cgi
RUN apk add libxml2-utils
CMD ["httpd","-D","FOREGROUND"] 
