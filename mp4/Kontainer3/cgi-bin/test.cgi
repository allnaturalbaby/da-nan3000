#!/bin/bash
echo Content-type: text/html
echo

USERMAIL=`echo "$QUERY_STRING" | sed -n 's/^.*navn=\([^&]*\).*$/\1/p' | sed "s/+/ /g" | sed "s/%40/@/g"` 
PSW=`echo "$QUERY_STRING" | sed -n 's/^.*psw=\([^&]*\).*$/\1/p'`



 echo Variablen QUERY_STRING: $QUERY_STRING 
 echo MAIL: $USERMAIL
 echo PASSWORD: $PSW
 echo SERVER_PROTOCOL: $SERVER_PROTOCOL
 echo SERVER_PORT: $SERVER_PORT
 echo REQUEST_METHOD: $REQUEST_METHOD
 echo PATH_INFO: $PATH_INFO
 echo PATH_TRANSLATED: $PATH_TRANSLATED
 echo SCRIPT_NAME: $SCRIPT_NAME
 echo REMOTE_HOST: $REMOTE_HOST
 echo REMOTE_ADDR: $REMOTE_ADDR
 echo AUTH_TYPE: $AUTH_TYPE
 echo REMOTE_USER: $REMOTE_USER
 echo REMOTE_IDENT: $REMOTE_IDENT
 echo CONTENT_TYPE: $CONTENT_TYPE
 echo CONTENT_LENGTH: $CONTENT_LENGTH
 echo KAKE: $HTTP_COOKIE
 echo 

#curl -d "" 172.17.0.1:8180/cgi-bin/diktbase.cgi/logout
#curl -d "<user><username>$USERMAIL</username><password>$PSW</password></user>" 172.17.0.1:8180/cgi-bin/diktbase.cgi/login

function loggin() {
    curl -d "<user><username>$USERMAIL</username><password>$PSW</password></user>" -X POST 172.17.0.1:8180/cgi-bin/diktbase.cgi/login  
    echo
    echo Content-type:text/html;charset=utf-8
    echo

    
    cat << EOF
    <!doctype html>
    <html>
        <body>
            
        </body>    
    </html>
EOF
}
loggin

echo KAKE etter login: $HTTP_COOKIE
function loggout() {
    curl -d "" 172.17.0.1:8180/cgi-bin/diktbase.cgi/logout
}

function alleDikt() {
    RES=$(curl 172.17.0.1:8180/cgi-bin/diktbase.cgi/dikt -H "Content-Type: application/xml" -H "Accept: application/xml")
    echo $RES
}
# cat << EOF
# <!doctype html>
# <html>
# <body>

# </body>
# </html>
# EOF