#!/bin/bash

echo 1 >/proc/sys/net/ipv4/conf/all/arp_ignore;
echo 2 >/proc/sys/net/ipv4/conf/all/arp_announce;
{% for vip in vips %}
/sbin/ifconfig lo:{{loop.index}} {{vip}} netmask 255.255.255.255 up
{% endfor %}
