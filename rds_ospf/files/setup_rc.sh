#!/bin/bash

if grep arp_announce /etc/rc.d/rc.local
then
	echo 'already setup'
	exit
fi

cat <<EOF >> /etc/rc.d/rc.local
echo 1 >/proc/sys/net/ipv4/conf/all/arp_ignore;
echo 2 >/proc/sys/net/ipv4/conf/all/arp_announce;
ifconfig lo:1 106.120.184.177 netmask 255.255.255.255 up
ifconfig lo:2 111.206.234.50 netmask 255.255.255.255 up
EOF

touch /etc/quagga/rc.local.created
