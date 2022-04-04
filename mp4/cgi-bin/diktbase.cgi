#!/bin/bash
read BODY

### Variables ###
database_path=../../diktbase.db
url_path=$REQUEST_URI
url_base=$(basename "$url_path") #last part of url, after last /
cookie=$HTTP_COOKIE
currentEmail=""
currentSessionId=""
sessionId=""
isLoggedIn="0"
response=""
length=""

#Function to check if user is logged in
function checkIfLoggedIn() {

	IFS="=" #Set delimeter
	read -a cookieArray <<<$cookie
	IFS='\' #Reset delimeter

	cookieSessionId=${cookieArray[1]}

	#cookieSessionId="814044c3-0d58-4554-aeeb-b40d491d2639"

	databaseSession=$(sqlite3 $database_path "SELECT * FROM sesjon WHERE sesjonsID = '$cookieSessionId';")

	#echo $databaseSession

	if [ -z $databaseSession ]; then #If not logged in
		isLoggedIn="0"

	else	#If logged in
		IFS="|"
		read session email <<<"$databaseSession"
		IFS='\'

		currentSessionId="$session"
		currentEmail="$email"
		isLoggedIn="1"
	fi
}


if [ "$REQUEST_METHOD" = "GET" ]; then

	IFS='/' #Set delimeter
	read -a url_array <<<"$url_path" 	#Making an array of url: parts on every /
	IFS='\' #Reset delimeter


	#Get all poems
	if [ ${url_array[3]} = "dikt" -a -z "${url_array[4]}" ]; then				#if index 3 is "dikt" and index 4 is empty string
		poems=$(sqlite3 $database_path "SELECT * FROM dikt;")

		allPoemsInXml=""

		IFS=$'\n'
		for poem in $poems;
		do
			allPoemsInXml+=$(echo "<dikt>")
			allPoemsInXml+=$(echo "<diktID>$(echo $poem | cut -d '|' -f1)</diktID>")
			allPoemsInXml+=$(echo "<tekst>$(echo $poem | cut -d '|' -f2)</tekst>")
			allPoemsInXml+=$(echo "<epostadresse>$(echo $poem | cut -d '|' -f3)</epostadresse>") 
			allPoemsInXml+=$(echo "</dikt>")
		done
		IFS='\'

		response="<?xml version=\"1.0\" encoding=\"UTF-8\"?>"
		response+="<?xml-stylesheet href=\"http://localhost/diktbaseStyle.css\"?>"
		response+="<!DOCTYPE response SYSTEM \"http://localhost/diktbase.dtd\">"
		response+="<diktbase>"$allPoemsInXml"</diktbase>"
		length=${#response}
	
	#Get one poem
	elif [ ${url_array[3]} = "dikt" -a ${url_array[4]} = $url_base ]; then		#if index 3 is "dikt" and index 4 is equal to last /something
		onePoem=$(sqlite3 $database_path "SELECT * FROM dikt WHERE diktID=$url_base;")

		IFS="|"
		read -a poemArray <<<$onePoem
		IFS='\'

		response="<?xml version=\"1.0\" encoding=\"UTF-8\"?>"
		response+="<?xml-stylesheet href=\"http://localhost/diktbaseStyle.css\"?>"
		response+="<!DOCTYPE response SYSTEM \"http://localhost/diktbase.dtd\">"
		response+="<diktbase><dikt><diktID>"${poemArray[0]}"</diktID><tekst>"${poemArray[1]}"</tekst><epostadresse>"${poemArray[2]}"</epostadresse></dikt></diktbase>"
		length=${#response}
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
			response="<?xml version=\"1.0\" encoding=\"UTF-8\"?>"
			response+="<!DOCTYPE response SYSTEM \"http://localhost/response.dtd\">"
			response+="<response><status>0</status><statustext>Brukernavn eller passord er feil</statustext><sessionid></sessionid><user></user></response>"
			length=${#response}
			
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

					response="<?xml version=\"1.0\" encoding=\"UTF-8\"?>"
					response+="<!DOCTYPE response SYSTEM \"http://localhost/response.dtd\">"
					response+="<response><status>1</status><statustext>Du er logget inn</statustext><sessionid>"$sessionId"</sessionid><user>"$currentUser"</user></response>"
					length=${#response}
						

				else	#If sessionId does exist, so duplicates doesn't happen
					response="<?xml version=\"1.0\" encoding=\"UTF-8\"?>"
					response+="<!DOCTYPE response SYSTEM \"http://localhost/response.dtd\">"
					response+="<response><status>0</status><statustext>Noe gikk galt, prøv igjen</statustext><sessionid></sessionid><user></user></response>"
					length=${#response}
						
				fi

			else	#If password is not correct
				response="<?xml version=\"1.0\" encoding=\"UTF-8\"?>"
				response+="<!DOCTYPE response SYSTEM \"http://localhost/response.dtd\">"
				response+="<response><status>0</status><statustext>Brukernavn eller passord er feil</statustext><sessionid></sessionid><user></user></response>"
				length=${#response}
					
			fi
		fi

	#Log out
	elif [ ${url_array[3]} = 'logout' -a $isLoggedIn = 1 ]; then

		#xmlInput=$BODY
		#loggedInSessionId=$(xmllint --xpath "//sessionid/text()" - <<<"$xmlInput") #Getting sessionid from bodyparameter in xml

		#echo $loggedInSessionId

		sqlite3 $database_path "DELETE FROM sesjon WHERE sesjonsID='$currentSessionId';"

		response="<?xml version=\"1.0\" encoding=\"UTF-8\"?>"
		response+="<!DOCTYPE response SYSTEM \"http://localhost/response.dtd\">"
		response+="<response><status>1</status><statustext>Bruker logget ut</statustext><sessionid>"$currentSessionId"</sessionid><user>"$currentEmail"</user></response>"
		length=${#response}
			
		

	#Create poem
	elif [ ${url_array[3]} = "dikt" -a $isLoggedIn = 1 ]; then	#Post to make new poem localhost/cgi-bin/diktbase.cgi/dikt
			
		xmlInput=$BODY													
		newPoem=$(xmllint --xpath "//tekst/text()" - <<<"$xmlInput")		#Getting new poem from bodyparameter in xml


		lastId=$(sqlite3 $database_path "SELECT diktID FROM dikt ORDER BY diktID DESC LIMIT 1;")	#Getting last id that exists
		let "newId = $lastId + 1"																	#Making new id from last id

		sqlite3 $database_path "INSERT INTO dikt VALUES('$newId', '$newPoem', '$currentEmail');"	#Inserting the new poem

		response="<?xml version=\"1.0\" encoding=\"UTF-8\"?>"
		response+="<!DOCTYPE response SYSTEM \"http://localhost/response.dtd\">"
		response+="<response><status>1</status><statustext>Nytt dikt lagret</statustext><sessionid>"$currentSessionId"</sessionid><user>"$currentEmail"</user></response>"
		length=${#response}
			
	else	
		response="<?xml version=\"1.0\" encoding=\"UTF-8\"?>"
		response+="<!DOCTYPE response SYSTEM \"http://localhost/response.dtd\">"
		response+="<response><status>0</status><statustext>Feil adresse</statustext><sessionid></sessionid><user></user></response>"
		length=${#response}	
	fi
fi


#PUT
if [ "$REQUEST_METHOD" = "PUT" ]; then

	checkIfLoggedIn
    
	IFS='/' #Set delimeter
	read -a url_array <<<"$url_path"
	IFS='\' #Reset delimeter

	if [ $isLoggedIn = 1 ]; then

		#Change poem
		if [ ${url_array[4]} = $url_base ]; then

			xmlInput=$BODY													
			poemChanged=$(xmllint --xpath "//tekst/text()" - <<<"$xmlInput")
				
			sqlite3 $database_path "UPDATE dikt SET dikt='$poemChanged' WHERE diktID='$url_base';"

			response="<?xml version=\"1.0\" encoding=\"UTF-8\"?>"
			response+="<!DOCTYPE response SYSTEM \"http://localhost/response.dtd\">"
			response+="<response><status>1</status><statustext>Dikt "$url_base" endret</statustext><sessionid>"$loggedInSessionId"</sessionid><user>"$currentUser"</user></response>"
			length=${#response}
			

		else
			response="<?xml version=\"1.0\" encoding=\"UTF-8\"?>"
			response+="<!DOCTYPE response SYSTEM \"http://localhost/response.dtd\">"
			response+="<response><status>0</status><statustext>Feil adresse</statustext><sessionid></sessionid><user></user></response>"
			length=${#response}
		fi

	else
		response="<?xml version=\"1.0\" encoding=\"UTF-8\"?>"
		response+="<!DOCTYPE response SYSTEM \"http://localhost/response.dtd\">"
		response+="<response><status>0</status><statustext>Bruker må være logget inn for å gjennomføre denne handlingen</statustext><sessionid></sessionid><user></user></response>"
		length=${#response}
		
	fi
fi


if [ "$REQUEST_METHOD" = "DELETE" ]; then

	checkIfLoggedIn
    
	IFS='/' #Set delimeter
	read -a url_array <<<"$url_path"
	IFS='\' #Reset delimeter


	if [ $isLoggedIn = 1 ]; then
		#Slett alle egne dikt
		if [ ${url_array[3]} = "dikt" -a -z "${url_array[4]}" ]; then

		

			sqlite3 $database_path "DELETE FROM dikt WHERE epostadresse='$currentEmail';"

			response="<?xml version=\"1.0\" encoding=\"UTF-8\"?>"
			response+="<!DOCTYPE response SYSTEM \"http://localhost/response.dtd\">"
			response+="<response><status>1</status><statustext>Alle dikt tilhørende: "$currentEmail" slettet</statustext><sessionid>"$loggedInSessionId"</sessionid><user>"$currentUser"</user></response>"
			length=${#response}
			

		#Slett dikt med $id
		elif [ ${url_array[3]} = "dikt" -a ${url_array[4]} = $url_base ]; then

			sqlite3 $database_path "DELETE FROM dikt WHERE diktID='$url_base';"

			response="<?xml version=\"1.0\" encoding=\"UTF-8\"?>"
			response+="<!DOCTYPE response SYSTEM \"http://localhost/response.dtd\">"
			response+="<response><status>1</status><statustext>Dikt "$url_base" slettet</statustext><sessionid>"$loggedInSessionId"</sessionid><user>"$currentUser"</user></response>"
			length=${#response}
			
		
		#Hvis nettadressen ikke eksisterer?
		else
			response="<?xml version=\"1.0\" encoding=\"UTF-8\"?>"
			response+="<!DOCTYPE response SYSTEM \"http://localhost/response.dtd\">"
			response+="<response><status>0</status><statustext>Feil adresse</statustext><sessionid></sessionid><user></user></response>"
			length=${#response}
			
		fi
	else 
		response="<?xml version=\"1.0\" encoding=\"UTF-8\"?>"
		response+="<!DOCTYPE response SYSTEM \"http://localhost/response.dtd\">"
		response+="<response><status>0</status><statustext>Bruker må være logget inn for å gjennomføre denne handlingen</statustext><sessionid></sessionid><user></user></response>"
		length=${#response}
		
	fi
fi



if [ ${#sessionId} -gt "0" ]; then
	echo "Set-Cookie:sessionId="$sessionId"; SameSite=None; Secure"
	echo "Content-Length: "$length
	echo "Content-type:application/xml;charset=utf-8"
	echo "Access-Control-Allow-Origin: http://localhost"
	echo "Access-Control-Allow-Credentials: true"
	echo "Access-Control-Allow-Methods: POST,PUT,DELETE,GET"
	echo
	echo $response
else
	echo "Content-Length: "$length
	echo "Content-type:application/xml;charset=utf-8"
	echo "Access-Control-Allow-Origin: http://localhost"
	echo "Access-Control-Allow-Credentials: true"
	echo "Access-Control-Allow-Methods: POST,PUT,DELETE,GET"
	echo
	echo $response
fi



