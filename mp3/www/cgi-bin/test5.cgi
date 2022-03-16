#!/bin/bash

read BODY

# Skriver ut 'http-header' for 'plain-text'
echo "Content-type:application/xml;charset=utf-8"

# Skriver ut tom linje for å skille hodet fra kroppen
echo

#echo REQUEST_URI:    $REQUEST_URI 
#echo REQUEST_METHOD: $REQUEST_METHOD
#echo

### Variables ###
database_path=../../diktbase.db
url_path=$REQUEST_URI
url_base=$(basename "$url_path") #last part of url, after last /



if [ "$REQUEST_METHOD" = "GET" ]; then

	IFS='/' #Set delimeter
	read -a url_array <<<"$url_path" 	#Making an array of url: parts on every /
	IFS='\' #Reset delimeter


	if [ ${url_array[3]} = "dikt" -a -z "${url_array[4]}" ]; then				#if index 3 is "dikt" and index 4 is empty string
		sqlite3 $database_path "SELECT * FROM dikt;" | awk -F'|' '
		{ diktID[++i]=$1; dikt[i]=$2; epostadresse[i]=$3 }
        END {
            printf "<diktbase>";
            for(j=1;j<=i;j++){
                printf "<dikt>"
                printf "<diktID>%s</diktID>",diktID[j]
                printf "<dikt>%s</dikt>",dikt[j]
                printf "<epostadresse>%s</epostadresse>",epostadresse[j]
                printf "</dikt>"
            }
            printf "</diktbase>";
        }'
	
	elif [ ${url_array[3]} = "dikt" -a ${url_array[4]} = $url_base ]; then		#if index 3 is "dikt" and index 4 is equal to last /something
		sqlite3 $database_path "SELECT * FROM dikt WHERE diktID=$url_base;" | awk -F'|' '
		{ diktID[++i]=$1; dikt[i]=$2; epostadresse[i]=$3 }
        END {
            printf "<diktbase>";
            for(j=1;j<=i;j++){
                printf "<dikt>"
                printf "<diktID>%s</diktID>",diktID[j]
                printf "<dikt>%s</dikt>",dikt[j]
                printf "<epostadresse>%s</epostadresse>",epostadresse[j]
                printf "</dikt>"
            }
            printf "</diktbase>";
        }'
	fi
fi

if [ "$REQUEST_METHOD" = "POST" ]; then

	IFS='/' #Set delimeter
	read -a url_array <<<"$url_path"
	IFS='\' #Reset delimeter



	#Login
	if [ ${url_array[3]} = "login" ]; then

		xmlInput=$BODY
        username=$(xmllint --xpath "//username/text()" - <<<"$xmlInput") # Parsing xml user
        password=$(xmllint --xpath "//password/text()" - <<<"$xmlInput") # Parsing xml password
	

		user=$(sqlite3 $database_path "SELECT * FROM bruker WHERE epostadresse='$username';")
		

		if [ -z $user ]; then	#If user does not exist
			response="<?xml version="1.0"?>"
			response+="<!DOCTYPE response SYSTEM "http://localhost/response.dtd">"
			response+="<response><status>0</status><statustext>Brukernavn eller passord er feil</statustext><sessionid></sessionsid><user></user></response>"
			length=${#response}
			echo "Content-Length: "$length
			echo
			echo $response


		else					#If user exist
			IFS='|'
			read userEmail userPassword userFname userLname <<< "$user"
			IFS='\'

			currentUser=$userEmail
			currentUserPassword=$userPassword

			hashpassword=$(echo -n $password | sha512sum | head -n 1 )

			if [ $hashpassword = $currentUserPassword ]; then		#If password is correct
				sessionId=$(uuidgen -r)	
				
				existingSessions=$(sqlite3 $database_path "SELECT sesjonsID FROM sesjon WHERE sesjonsID='$sessionId';")
				doesSessionExist=${#existingSessions}

				if [ $doesSessionExist = 0 ]; then				#If sessionId does not exist 
					sqlite3 $database_path "INSERT INTO sesjon (sesjonsID,epostadresse) \
					VALUES(\"$sessionId\",\"$currentUser\");"

					response="<?xml version="1.0"?>"
					response+="<!DOCTYPE response SYSTEM "http://localhost/response.dtd">"
					response+="<response><status>1</status><statustext>Du er logget inn</statustext><sessionid>"$sessionId"</sessionid><user>"$currentUser"</user></response>"
					length=${#response}
					echo "Content-Length: "$length
					echo
					echo $response

				else	#If sessionId does exist, so duplicates doesn't happen
					response="<?xml version="1.0"?>"
					response+="<!DOCTYPE response SYSTEM "http://localhost/response.dtd">"
					response+="<response><status>0</status><statustext>Noe gikk galt, prøv igjen</statustext><sessionid></sessionid><user></user></response>"
					length=${#response}
					echo "Content-Length: "$length
					echo
					echo $response
				fi

			else													#If password is not correct
				response="<?xml version="1.0"?>"
				response+="<!DOCTYPE response SYSTEM "http://localhost/response.dtd">"
				response+="<response><status>0</status><statustext>Brukernavn eller passord er feil</statustext><sessionid></sessionid><user></user></response>"
				length=${#response}
				echo "Content-Length: "$length
				echo
				echo $response
			fi
		fi

	fi

	if [ ${url_array[3]} = 'logout' ]; then
		echo "logout"

		xmlInput=$BODY
        loggedInSessionId=$(xmllint --xpath "//sessionid/text()" - <<<"$xmlInput") # Parsing xml sessionid

		echo $loggedInSessionId

		sqlite3 $database_path "DELETE FROM sesjon WHERE sesjonsID='$loggedInSessionId';"

		response="<?xml version="1.0"?>"
		response+="<!DOCTYPE response SYSTEM "http://localhost/response.dtd">"
		response+="<response><status>1</status><statustext>Bruker logget ut</statustext><sessionid>"$loggedInSessionId"</sessionid><user>"$currentUser"</user></response>"
		length=${#response}
		echo "Content-Length: "$length
		echo
		echo $response
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

