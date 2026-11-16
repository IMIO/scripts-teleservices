#!/bin/bash
# WEB-4156: Randomize the minute of the cron job "tenant_command cron"
cur_brick="combo"
uwsgi_ini_path="/etc/combo/uwsgi.ini"
minute=$((RANDOM % 59 + 1))
original_line=$(grep "combo-manage tenant_command cron" $uwsgi_ini_path)
sed -i "/combo-manage tenant_command cron/ s/minute=[^,]*,/minute=$minute,/" $uwsgi_ini_path
modified_line=$(grep "combo-manage tenant_command cron" $uwsgi_ini_path)
echo "✨ WEB-4156 ($cur_brick) · Original line: $original_line"
echo "🔁 WEB-4156 ($cur_brick) · Modified line: $modified_line"