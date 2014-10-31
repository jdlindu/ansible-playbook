#!/bin/bash

if grep arp_announce /etc/rc.d/rc.local
then
	echo 'already setup'
	exit
fi

cat <<EOF >> /etc/rc.d/rc.local
echo 1 >/proc/sys/net/ipv4/conf/all/arp_ignore;
echo 2 >/proc/sys/net/ipv4/conf/all/arp_announce;
{% for vip in vips %}
ifconfig lo:{{loop.index}} {{vip}} netmask 255.255.255.255 up
{% endfor %}
EOF

touch /etc/quagga/rc.local.created
