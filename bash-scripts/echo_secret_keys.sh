#!/bin/bash
# Helps to resolve INFRA-4237 TELE-1236

BRICKS=('/etc/chrono/secret' '/etc/bijoe/secret' '/etc/hobo/secret' '/etc/passerelle/secret/' '/etc/combo/secret' '/etc/fargo/secret' '/etc/authentic2-multitenant/secret' '/etc/wcs/secret')

for el in "${BRICKS[@]}"
do
	echo $'\n'
	echo $el;
	cat $el
	echo $'\n'
done
