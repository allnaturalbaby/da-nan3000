#!/bin/sh
echo "Content-type:text/html;charset=utf-8"
echo

read body

cat << EOF
<!doctype html>
<html>
	<head>
	<meta charset='utf-8'>
	<title>Test2</title>
	</head>
	<body>
		<form method='post'>
			<input type=text name=fornavn placeholder='fornavn' >
			<br>
			<input type=text name=etternavn placeholder='etternavn' >
			<br>
			<input type=submit>
		</form>
		<pre>
		Info om HTTP-forespørsel:
		-------------------------
		Kroppen innhold: $BODY
		Metode: 	 $REQUEST_METHOD
		Kroppens lengde: $CONTENT_LENGTH
		</pre>
	</body>
</html>
EOF
