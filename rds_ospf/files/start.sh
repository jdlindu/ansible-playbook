#!/bin/bash

echo 1 >/proc/sys/net/ipv4/conf/all/arp_ignore;
echo 2 >/proc/sys/net/ipv4/conf/all/arp_announce;
/sbin/ifconfig lo:1 101.226.6.226 netmask 255.255.255.255 up
