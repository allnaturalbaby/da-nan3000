FROM mp4docker

RUN apk add curl && apk add libxml2-utils && apk add util-linux

COPY ./cgi-bin/* /usr/local/apache2/cgi-bin/

RUN chmod 755 /usr/local/apache2/cgi-bin/

CMD ["httpd","-D","FOREGROUND"]

