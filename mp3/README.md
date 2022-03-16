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



### Logge inn
```
Url: https://localhost/cgi-bin/test5.cgi/login
Metode: POST
Bodyparameter: <user><username></username><password></password></user> 
Header: Content-type: application/xml
Respons: <response><status></status><statustext></statustext><sessionid></sessionid><user></user></response>
```

### Logge ut
```
Url: https://localhost/cgi/bin/test5.cgi/logout
Metode: POST
Bodyparameter: <user><sessionid></sessionid><user> 
Header: Content-type: application/xml
Respons: <response><status></status><statustext></statustext><sessionid></sessionid><user></user></response>
```

### Hente ett dikt
```
Url: https://localhost/cgi-bin/test5.cgi/dikt/$id
Metode: GET
Bodyparameter: ""
Header: Content-type: application/xml
Respons: <diktbase><dikt><diktID></diktID><dikt></dikt><epostadresser></epostadresse></dikt></diktbase>
```

### Hente alle dikt
```
Url: https://localhost/cgi-bin/test5.cgi/dikt
Metode: GET
Bodyparameter: "" 
Header: Content-type: application/xml
Respons: <diktbase><dikt><diktID></diktID><dikt></dikt><epostadresser></epostadresse></dikt></diktbase>
```

### Endre dikt
```
Url: https://localhost/
Metode:
Bodyparameter: 
Header:
Respons:
```

### Legge til dikt
```
Url: https://localhost/
Metode:
Bodyparameter: 
Header:
Respons:
```

### Slette ett dikt
```
Url: https://localhost/
Metode:
Bodyparameter: 
Header:
Respons:
```

### Slette alle egne dikt
```
Url: https://localhost/
Metode:
Bodyparameter: 
Header:
Respons:
```
