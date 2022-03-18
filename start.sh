#!/bin/bash
if [ -z "$1" ]
    then
        echo "Spesifiser hvilken mp du vil bruke. feks, sudo ./start mp1"
        exit 1
fi

if [ $1 = "-h" ]
    then
        echo "How do i do the thing:"
        echo -e "\t-h for hjelp\n\tmp1 for milepæl 1 osv\n\tDisse må være lik som filstrukturen du har filene i.\n\tMappen scripts må også være tilgjengelig.\n\tMå også være sudo"
        exit 1
fi

if [[ "$(whoami)" != root ]]
    then
        echo "Du må kjøre som sudo"
        exit 1
fi


cd $1
./scripts/kill.sh
sudo ./scripts/create_log.sh
gcc improved.c -o improved
sudo ./improved

echo "Have a nice day /redacted/ ;]"
exit 0