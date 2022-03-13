#!/bin/bash

read BODY

# Skriver ut 'http-header' for 'plain-text'
echo "Content-type:text/plain;charset=utf-8"

# Skriver ut tom linje for å skille hodet fra kroppen
echo


echo REQUEST_URI:    $REQUEST_URI 
echo REQUEST_METHOD: $REQUEST_METHOD
echo

### Variables ###
database_path=../../diktbase.db
url_path=$REQUEST_URI
dikt_path=/cgi-bin/test5.cgi/dikt
url_base=$(basename "$url_path")



if [ "$REQUEST_METHOD" = "GET" ]; then


	if [ "$url_base" = "dikt" ]; then
		sqlite3 $database_path  "SELECT * FROM dikt;"
	elif [ "$REQUEST_URI" = "$dikt_path/$url_base" ]; then
		sqlite3 $database_path "SELECT * FROM dikt WHERE diktID=$url_base;"
	else
		echo Something went wrong
	fi
fi

if [ "$REQUEST_METHOD" = "POST" ]; then

	if [ "$url_base" = "login" ]; then
		echo login

		bodyinput=$BODY
		username=$bodyinput
		#password=$bodyinput
		echo $username
		#echo $password
	fi


fi

if [ "$REQUEST_METHOD" = "PUT" ]; then
    echo $REQUEST_URI skal endres slik:
    echo

    # skriver-hode
    head -c $CONTENT_LENGTH
    echo 
fi

if [ "$REQUEST_METHOD" = "DELETE" ]; then
    echo $REQUEST_URI skal slettes
fi

