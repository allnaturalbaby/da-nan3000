# Lage "How to start all and stuff here"

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