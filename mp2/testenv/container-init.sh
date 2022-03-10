#!/bin/bash

CONFS=$PWD/container

if [ ! -d $CONFS ];then

    mkdir -p $CONFS/{bin,proc,etc,var/www,var/log}
    cp -r ../pages_/ $CONFS/var/www/
    gcc ../improved.c -o $CONFS/bin/improved
    ls -la $CONFS/bin | grep improved
    touch $CONFS/bin/log.txt
    #chown 1000:1000 $CONFS/bin/debug.log
    echo "pussy" > $CONFS/bin/log.txt

    echo test1

    cd       $CONFS/bin/
    cp       /bin/busybox .

    for P in $(./busybox --list | grep -v busybox); do ln busybox $P; done;

    echo test2

    #echo "::once:/bin/httpd -p 8080 -h /var/www" >  $ROTFS/etc/inittab
    echo "::once:/sbin/improved" > $CONFS/etc/inittab

    echo test3

    #echo "hallo" >  $ROTFS/var/www/hallo.txt
    #echo $PWD
    #cp -r $PWD/pages $ROTFS/var/www/
    
    #exit 1
    echo $CONFS
fi

echo test4
#sudo PATH=/bin unshare -f -p --mount-proc /usr/sbin/chroot $ROTFS bin/init

sudo PATH=/bin unshare -f -p --mount-proc /usr/sbin/chroot $CONFS bin/init

#  # Inspisere:
#  pstree -p UNSHARE_PID
#  ps -o pid,ppid,uid,tty,cmd PID1 PID2 ...

#  # teste: 
#  curl localhost:8080/hallo.txt

#  # Starte et shell med (alle) samme naverom som PID
#  sudo nsenter -t PID -a
