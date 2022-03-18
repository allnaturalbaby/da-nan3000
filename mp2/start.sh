cd testenv
rm -r container

AUXPID=$(ps aux | less | grep ./improved | head -1 | awk '{ print $2 }')
kill -9 $AUXPID

JOBPID=$(jobs -p | awk '{ print $3 }')   
kill -9 $JOBPID

./container-init.sh

echo "Have a nice day /redacted/ ;]"