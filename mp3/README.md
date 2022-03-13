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


