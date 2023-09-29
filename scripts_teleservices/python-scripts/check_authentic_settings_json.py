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
        tenant = tenant.strip()
        slug = tenant.split("_", maxsplit=1)[0]

        # Construct full path to settings.json
        settings_path = os.path.join(dir_path, tenant, "settings.json")

        # Check if settings.json exists
        if not os.path.exists(settings_path):
            print(f"MISSING {settings_path}")
        else:
            # load settings.json and verify that THEME_SKELETON_URL value contains the slug
            with open(settings_path, "r") as settings_file:
                settings = settings_file.read()
                if slug not in settings:
                    print(f"ERROR {settings_path}")
