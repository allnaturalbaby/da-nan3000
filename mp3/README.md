OVERSKRIFT

Apache2
Endre cgi-bin i /etc/apache2/conf.available/serve-cgi-bin.conf til www/cgi-bin mappen i mp3
Endre DocumentRoot i /etc/apache2/sites-available/000-default.conf til www mappen i mp3
Endre Directory path i /etc/apache2/apache2.conf til www mappen i mp3
sudo a2enmod cgi //For å la cgi-script kjøre i nettleser
sudo service apache2 restart

For å opprette database med eksempeldata:
./creatediktbase.sh

Opprette kun database:
sqlite3 diktbase.db < diktbase.sql

Legge eksempeldata til i database(databasen må eksistere):
sqlite3 diktbase.db < eksempeldata.sql

Brukere: 
Epost: nora@hvcn.com Passord: Passord1
Epost: hevos@hvcn.com Passord: Passord2
Epost: viktor@hvcn.com Passord: Passord3
Epost: christian@hvcn.com Passord: Passord4



### Hente ett dikt
```
Url: https://localhost/cgi-bin/diktbase.cgi/dikt/$id
Metode: GET
Bodyparameter: ""
Header: Content-type: application/xml
Respons: <diktbase><dikt><diktID></diktID><dikt></dikt><epostadresser></epostadresse></dikt></diktbase>
```

### Hente alle dikt
```
Url: https://localhost/cgi-bin/diktbase.cgi/dikt
Metode: GET
Bodyparameter: "" 
Header: Content-type: application/xml
Respons: <diktbase><dikt><diktID></diktID><dikt></dikt><epostadresser></epostadresse></dikt></diktbase>
```

### Logge inn
```
Url: https://localhost/cgi-bin/diktbase.cgi/login
Metode: POST
Bodyparameter: <user><username></username><password></password></user> 
Header: Content-type: application/xml
Respons: <response><status></status><statustext></statustext><sessionid></sessionid><user></user></response>
```

### Logge ut
```
Url: https://localhost/cgi/bin/diktbase.cgi/logout
Metode: POST
Bodyparameter: ""
Header: Content-type: application/xml
Respons: <response><status></status><statustext></statustext><sessionid></sessionid><user></user></response>
```

### Lage nytt dikt
```
Url: https://localhost/cgi-bin/diktbase.cgi/dikt
Metode: POST
Bodyparameter: <dikt><tekst></tekst></dikt>
Header: Content-type: application/xml
Respons: <response><status></status><statustext></statustext><sessionid></sessionid><user></user></response>
```

### Endre dikt
```
Url: https://localhost/cgi-bin/diktbase.cgi/dikt/$id
Metode: PUT
Bodyparameter: <dikt><tekst></tekst></dikt>
Header: Content-type: application/xml
Respons: 
```

### Slette ett dikt
```
Url: https://localhost/cgi-bin/diktbase.cgi/dikt/$id
Metode: DELETE
Bodyparameter: ""
Header: Content-type: application/xml
Respons: <response><status></status><statustext></statustext><sessionid></sessionid><user></user></response>
```

### Slette alle egne dikt
```
Url: https://localhost/cgi-bin/diktbase.cgi/dikt
Metode: DELETE
Bodyparameter: ""
Header: Content-type: application/xml
Respons: <response><status></status><statustext></statustext><sessionid></sessionid><user></user></response>
```
