#!/bin/sh

cat <<EOF
Content-type: application/xml; charset=utf-8

<?xml version="1.0"?>
<?xml-stylesheet type="text/xsl" href="/alledikt.xsl"?>

<tabell>
<rad>
EOF

echo -n 'SELECT * FROM dikt;' | \
	sqlite3 ../diktbase.db -line | \
	sed 's/[[:blank:]]*\(.*\) = \(.*$\)/\t<felt navn="\1">\2 <\/felt>/' | \
	sed 's/^$/  <\/rad>\n <rad>/'

cat <<EOF
</rad>
</tabell>
EOF
