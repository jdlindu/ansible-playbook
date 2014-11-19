#!/bin/bash


OS=$(lsb_release -si)

if [ "$OS" == "Ubuntu" ]
then
	rc_file='/etc/rc.local'
else
	rc_file='/etc/rc.d/rc.local'
fi

if grep arp_announce $rc_file
then
	echo 'already setup'
	exit
fi

cat <<EOF >> $rc_file
echo 1 >/proc/sys/net/ipv4/conf/all/arp_ignore;
echo 2 >/proc/sys/net/ipv4/conf/all/arp_announce;
{% for vip in vips %}
ifconfig lo:{{loop.index}} {{vip}} netmask 255.255.255.255 up
{% endfor %}
EOF

touch /etc/quagga/rc.local.created
