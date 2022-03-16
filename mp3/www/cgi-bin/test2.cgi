#!/bin/sh

cat <<EOF
Content-type: application/xml; charset=utf-8

<?xml version="1.0"?>


<tabell>
 <rad>
EOF

echo -n 'select * from dikt;'                             | \
     sqlite3 ../../diktbase.db -line                             | \
     sed 's/[[:blank:]]*\(.*\) = \(.*$\)/\t<felt navn="\1">\2 <\/felt>/' | \
     sed 's/^$/  <\/rad>\n  <rad>/'

cat <<EOF
   </rad>
 </tabell>
EOF
