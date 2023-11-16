#!/bin/bash
ps faux | grep 'imio_indus_deploy' | awk '{print $2}' | xargs kill
