#!/bin/bash
echo"Content-type:text/html"
echo

USERMAIL=`echo "$QUERY_STRING" | sed -n 's/^.*navn=\([^&]*\).*$/\1/p' | sed "s/+/ /g" | sed "s/%40/@/g"` 
PSW=`echo "$QUERY_STRING" | sed -n 's/^.*psw=\([^&]*\).*$/\1/p'`



# echo Variablen QUERY_STRING: $QUERY_STRING 
# echo $USERMAIL
# echo $PSW
# echo "end of file"

#curl -d "" 172.17.0.1:8180/cgi-bin/diktbase.cgi/logout
#curl -d "<user><username>$USERMAIL</username><password>$PSW</password></user>" 172.17.0.1:8180/cgi-bin/diktbase.cgi/login

function loggin() {
    #  curl -d "<user><username>$USERMAIL</username><password>$PSW</password></user>" 172.17.0.1:80/cgi-bin/diktbase.cgi/login
    HTTP_CODE=$(curl -H "Content-Type: application/xml" -d "<user><username>$USERMAIL</username><password>$PSW</password></user>" localhost:8180/cgi-bin/diktbase.cgi/login)

}
loggin
echo $HTTP_CODE

# function loggout() {
#     curl -d "" 172.17.0.1:8180/cgi-bin/diktbase.cgi/logout
# }
# cat << EOF
# <!doctype html>
# <html>
# <body>

# </body>
# </html>
# EOF