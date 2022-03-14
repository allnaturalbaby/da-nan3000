#!/bin/bash

CONFS=$PWD/container

if [ ! -d $CONFS ];then

    mkdir -p $CONFS/{bin,proc,etc,var/www,var/log}
    cp -r ../pages_/ $CONFS/var/www/pages
    cp -r ../mimetypes_/ $CONFS/var/www/mimetypes
    gcc --static ../improved.c -o $CONFS/bin/improved.out
    
    #ls -la $CONFS/bin | grep improved
    
    touch $CONFS/var/log/log.txt

    #sudo chown 1000:1000 $CONFS/var/log/log.txt
    #sudo chown 1000:1000 $CONFS/bin/log.txt
    #chown 1000:1000 $CONFS/bin/debug.log

    cd       $CONFS/bin/
    cp       /bin/busybox .

    for P in $(./busybox --list | grep -v busybox); do ln busybox $P; done;

    echo "::once:/bin/improved.out" > $CONFS/etc/inittab

fi

#echo test4
#sudo PATH=/bin unshare -f -p --mount-proc /usr/sbin/chroot $ROTFS bin/init

sudo SHELL=/bin/sh PATH=/bin unshare -f -p --mount-proc /usr/sbin/chroot $CONFS bin/init

#  # Inspisere:
#  pstree -p UNSHARE_PID
#  ps -o pid,ppid,uid,tty,cmd PID1 PID2 ...

#  # teste: 
#  curl localhost:8080/hallo.txt

#  # Starte et shell med (alle) samme naverom som PID
#  sudo nsenter -t PID -a
