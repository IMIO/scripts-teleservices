#!/bin/bash

sed -i "s/0, 3/$(( (RANDOM % 60 ) )), $(( 2 + (RANDOM % 5) ))/" /usr/lib/python3/dist-packages/bijoe/uwsgi.py
service bijoe restart

