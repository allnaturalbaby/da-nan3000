#!/bin/bash

CONFS=$PWD/container

if [ ! -d $CONFS ];then

    mkdir -p $CONFS/{bin,proc,etc,var/www,var/log}
    cp -r ../pages_/ $CONFS/var/www/pages
    cp -r ../mimetypes_/ $CONFS/var/www/mimetypes
    cp -r ../response_/ $CONFS/var/www/response

    gcc --static ../improved.c -o $CONFS/bin/improved.out
    
    touch $CONFS/var/log/log.txt

    cd       $CONFS/bin/
    cp       /bin/busybox .

    for P in $(./busybox --list | grep -v busybox); do ln busybox $P; done;

    echo "::once:/bin/improved.out" > $CONFS/etc/inittab

fi

sudo SHELL=/bin/sh PATH=/bin unshare -f -p --mount-proc /usr/sbin/chroot $CONFS /bin/init
