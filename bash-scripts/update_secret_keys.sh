#!/bin/bash
# Helps to resolve INFRA-4237 TELE-1236

BRICKS=('/etc/chrono/secret' '/etc/bijoe/secret' '/etc/hobo/secret' '/etc/combo/secret' '/etc/fargo/secret' '/etc/authentic2-multitenant/secret' '/etc/wcs/secret')

for el in "${BRICKS[@]}"
do
	python3 -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())" > $el
done
