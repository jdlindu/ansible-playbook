#!/bin/bash

if [ "$#" -lt 2 ]
then
	echo "usage: $(echo $0) listening_ip port"
	exit 2
fi

listening_ip=$1
shift
ports=$*

for port in $ports
do
	nc -z -w1 0 $port || exit 2
done
