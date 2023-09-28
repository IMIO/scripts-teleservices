"""
20230928 - Check if settings.json is a symbolic link
This was generated to solve https://support.imio.be/browse/TELE-1800
"""
import os

# Path to the target directory
dir_path = "/var/lib/authentic2-multitenant/tenants/"

# Iterate through folders
for tenant in os.listdir(dir_path):
    if "auth" in tenant or "connexion" in tenant:
        # Construct full path to settings.json
        settings_path = os.path.join(dir_path, tenant, "settings.json")

        # Check if settings.json exists
        if os.path.exists(settings_path):
            # Check if it's a symbolic link
            if os.path.islink(settings_path):
                print(f"{settings_path} is a symbolic link.")
            else:
                print(f"{settings_path} is not a symbolic link.")
        else:
            print(f"{settings_path} does not exist.")
