AUXPID=$(ps aux | less | grep ./improved | head -1 | awk '{ print $2 }')
kill -SIGKILL $AUXPID

JOBPID=$(jobs -p | awk '{ print $3 }')   
kill -SIGKILL $JOBPID
