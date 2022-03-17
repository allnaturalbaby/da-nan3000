#!/bin/bash

read BODY

# Skriver ut 'http-header' for 'plain-text'
echo "Content-type:application/xml;charset=utf-8"
#echo "Set-Cookie:Noe=noeannet"

# Skriver ut tom linje for å skille hodet fra kroppen
echo

### Variables ###
database_path=../../diktbase.db
url_path=$REQUEST_URI
url_base=$(basename "$url_path") #last part of url, after last /
cookie=$HTTP_COOKIE
currentEmail=""
currentSessionId=""
isLoggedIn="0"

echo "HTTP_COOKIE:" $HTTP_COOKIE

function checkIfLoggedIn() {

	cookieSessionId="199dc93d-7ad0-443e-a4af-ebcd1bda82d7"

	databaseSession=$(sqlite3 $database_path "SELECT * FROM sesjon WHERE sesjonsID = '$cookieSessionId';")

	echo $databaseSession

	if [ -z $databaseSession ]; then #If not logged in
		isLoggedIn="0"

	else	#If logged in
		IFS="|"
		read session email <<<"$databaseSession
		IFS="\"

		currentSessionId="$session"
		currentEmail="$email"
		isLoggedIn="1"
	fi
}


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

	checkIfLoggedIn

	IFS='/' #Set delimeter
	read -a url_array <<<"$url_path"
	IFS='\' #Reset delimeter



	#Login
	if [ ${url_array[3]} = "login" -a $isLoggedIn = 0 ]; then

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

					echo "Set-Cookie:my_cookie=$sessionId"
					echo

					echo "Cookie:" $HTTP_COOKIE

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

			else	#If password is not correct
				response="<?xml version="1.0"?>"
				response+="<!DOCTYPE response SYSTEM "http://localhost/response.dtd">"
				response+="<response><status>0</status><statustext>Brukernavn eller passord er feil</statustext><sessionid></sessionid><user></user></response>"
				length=${#response}
				echo "Content-Length: "$length
				echo
				echo $response
			fi
		fi

	#Logg ut
	elif [ ${url_array[3]} = 'logout' -a $isLoggedIn = 1 ]; then

		xmlInput=$BODY
        loggedInSessionId=$(xmllint --xpath "//sessionid/text()" - <<<"$xmlInput") #Getting sessionid from bodyparameter in xml

		echo $loggedInSessionId

		sqlite3 $database_path "DELETE FROM sesjon WHERE sesjonsID='$loggedInSessionId';"

		response="<?xml version="1.0"?>"
		response+="<!DOCTYPE response SYSTEM "http://localhost/response.dtd">"
		response+="<response><status>1</status><statustext>Bruker logget ut</statustext><sessionid>"$currentSessionId"</sessionid><user>"$currentEmail"</user></response>"
		length=${#response}
		echo "Content-Length: "$length
		echo
		echo $response
	

	#Lage nytt dikt
	elif [ ${url_array[3]} = "dikt" -a $isLoggedIn = 1 ]; then	#Post to make new poem localhost/cgi-bin/diktbase.cgi/dikt
		
		xmlInput=$BODY													
		newPoem=$(xmllint --xpath "//text/text()" - <<<"$xmlInput")		#Getting new poem from bodyparameter in xml


		lastId=$(sqlite3 $database_path "SELECT diktID FROM dikt ORDER BY diktID DESC LIMIT 1;")	#Getting last id that exists
		let "newId = $lastId + 1"																	#Making new id from last id

		sqlite3 $database_path "INSERT INTO dikt VALUES('$newId', '$newPoem', 'norasophie96@hotmail.com');"	#Inserting the new poem

		response="<?xml version="1.0"?>"
		response+="<!DOCTYPE response SYSTEM "http://localhost/response.dtd">"
		response+="<response><status>1</status><statustext>Nytt dikt lagret</statustext><sessionid>"$currentSessionId"</sessionid><user>"$currentEmail"</user></response>"
		length=${#response}
		echo "Content-Length: "$length
		echo
		echo $response
	else	
		response="<?xml version="1.0"?>"
		response+="<!DOCTYPE response SYSTEM "http://localhost/response.dtd">"
		response+="<response><status>0</status><statustext>Feil adresse</statustext><sessionid></sessionid><user></user></response>"
		length=${#response}
		echo "Content-Length: "$length
		echo
		echo $response
	fi
fi


#PUT
if [ "$REQUEST_METHOD" = "PUT" ]; then

	checkIfLoggedIn
    
	IFS='/' #Set delimeter
	read -a url_array <<<"$url_path"
	IFS='\' #Reset delimeter

	if [ $isLoggedIn = 1 ]; then
	#Endre dikt
		if [ ${url_array[4]} = $url_base ]; then

			xmlInput=$BODY													
			poemChanged=$(xmllint --xpath "//text/text()" - <<<"$xmlInput")
			
			sqlite3 $database_path "UPDATE dikt SET dikt='$poemChanged' WHERE diktID='$url_base';"

			response="<?xml version="1.0"?>"
			response+="<!DOCTYPE response SYSTEM "http://localhost/response.dtd">"
			response+="<response><status>1</status><statustext>Dikt "$url_base" endret</statustext><sessionid>"$loggedInSessionId"</sessionid><user>"$currentUser"</user></response>"
			length=${#response}
			echo "Content-Length: "$length
			echo
			echo $response

		else
			response="<?xml version="1.0"?>"
			response+="<!DOCTYPE response SYSTEM "http://localhost/response.dtd">"
			response+="<response><status>0</status><statustext>Feil adresse</statustext><sessionid></sessionid><user></user></response>"
			length=${#response}
			echo "Content-Length: "$length
			echo
			echo $response
		fi
	fi
fi


if [ "$REQUEST_METHOD" = "DELETE" ]; then

	checkIfLoggedIn
    
	IFS='/' #Set delimeter
	read -a url_array <<<"$url_path"
	IFS='\' #Reset delimeter


	#Slett alle egne dikt
	if [ $isLoggedIn = 1 ]; then
		if [ ${url_array[3]} = "dikt" -a -z "${url_array[4]}" ]; then

			#currentUser="hevos@hvcn.com"

			sqlite3 $database_path "DELETE FROM dikt WHERE epostadresse='$currentUser';"

			response="<?xml version="1.0"?>"
			response+="<!DOCTYPE response SYSTEM "http://localhost/response.dtd">"
			response+="<response><status>1</status><statustext>Alle dikt tilhørende: "$currentUser" slettet</statustext><sessionid>"$loggedInSessionId"</sessionid><user>"$currentUser"</user></response>"
			length=${#response}
			echo "Content-Length: "$length
			echo
			echo $response

		#Slett dikt med $id
		elif [ ${url_array[3]} = "dikt" -a ${url_array[4]} = $url_base ]; then

			sqlite3 $database_path "DELETE FROM dikt WHERE diktID='$url_base';"

			response="<?xml version="1.0"?>"
			response+="<!DOCTYPE response SYSTEM "http://localhost/response.dtd">"
			response+="<response><status>1</status><statustext>Dikt "$url_base" slettet</statustext><sessionid>"$loggedInSessionId"</sessionid><user>"$currentUser"</user></response>"
			length=${#response}
			echo "Content-Length: "$length
			echo
			echo $response
		
		#Hvis nettadressen ikke eksisterer?
		else
			response="<?xml version="1.0"?>"
			response+="<!DOCTYPE response SYSTEM "http://localhost/response.dtd">"
			response+="<response><status>0</status><statustext>Feil adresse</statustext><sessionid></sessionid><user></user></response>"
			length=${#response}
			echo "Content-Length: "$length
			echo
			echo $response
		fi
	fi
fi

