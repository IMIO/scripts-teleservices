"""
Relates to INFRA-5293 and TELE-1800.
Allows to verify if the settings.json file is a symlink or not.
This will be executed evertwhere via rundeck.
"""
import os
import subprocess

authentic2_multitenant_path = "/var/lib/authentic2-multitenant/tenants/"
tenant = subprocess.run(["ls", authentic2_multitenant_path], stdout=subprocess.PIPE)
tenant = tenant.stdout.decode("utf-8").strip()
settings_json_path = f"{authentic2_multitenant_path}{tenant}/settings.json"


prefix = f"Tenant: {tenant} · "
if os.path.exists(settings_json_path):
    # Check if file is a symlink
    if os.path.islink(settings_json_path):
        print(f"{prefix}FIXME It's a symlink. Check manually.")
    else:
        print(f"{prefix}Seems fine.")
else:
    print("{prefix}File doesn't exist. Check manually.")
