#!/bin/bash

echo "Content-type:text/html;charset=utf-8"
echo 

read BODY

###Variables###
url_base=http://localhost:8180/cgi-bin/diktbase.cgi/
logged_in="1"


cat << EOF
    <!DOCTYPE html>
    <html>
    <head></head>
    <body>
EOF



if [ $logged_in == "0" ]; then
cat << EOF
            <h1>Hello World</h1>
            <form method="post" accept-charset="utf-8">
                <input type="text" name="email" placeholder="Epost" id="email">
                <input type="password" name="passw" placeholder="Passord" id="passw">
                <input type="submit" value="Logg inn">
            </form>
        </body>
    </html>
EOF
else
cat << EOF
            <h1>Hello World</h1>
            <form method="post" accept-charset="utf-8">
                <input type="submit" name="test" value="logout">
            </form>
EOF
fi
echo "Body: $BODY"

email=$(echo $BODY | sed s/%40/@/g | cut -f1 -d'&' | cut -f2 -d'=')
password=$(echo $BODY | cut -f3 -d'=')

#echo "Epost: $email <br>"
#echo "Passord: $password <br>"

if [ -z $BODY ]; then
   echo "No body yet"
else 
    info=$(curl -d "<user><username>$email</username><password>$password</password></user>" -X POST http://172.17.0.1:8180/cgi-bin/diktbase.cgi/login)
fi
echo $info
test=$(echo $info | cut -f1 -d'a')

echo $test

cat << EOF
    </body>
    </html>
EOF

