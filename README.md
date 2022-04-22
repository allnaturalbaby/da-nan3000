# How to start all and how to namespace

### Hvis apache2 kjører
```
service apache2 stop
```

## Starte Unshare containeren
```
./Unshare/testenv/container-init.sh
```

## Slette Unshare containeren
```
rm -r Unshare/testenv/container
killall -9 improved.out
```

## Starte Docker containerene
```
./Docker/Kontainer2/start.sh
./Docker/Kontainer3/start.sh
```

## Fjerne Docker containerene
```
./Docker/Kontainer2/fjern.sh
./Docker/Kontainer3/fjern.sh
```

## Nettsider
```
Hjemmeside: http://localhost
Diktdatabase javascript: http://localhost/app.html
Diktdatabase cgi-program: http://localhost:8080/cgi-bin/nytest.cgi
Dikt api (Dikt rett i nettleseren): http://localhost:8180/cgi-bin/diktbase.cgi/dikt
```

## Namespace til Kontainer 2 og 3
```
# Create user "remaper"
sudo adduser remaper

# Create group "remaper"
sudo addgroup remaper

# Add user "remaper" to the group "remaper"
sudo adduser container container

#Sett og/eller se group/user id 
$ cat /etc/subgid
remaper:400000:65536

$ cat /etc/subuid
remaper:400000:65536

#Set userns-remap til gruppen og bruker
/etc/docker/daemon.json
{
  "userns-remap": "remaper:remaper"
}

#Når kontainer kjører etter restart, se hvilken id som kjører det 
$ ps -ef | grep "httpd -D FOREGROUND"
```
