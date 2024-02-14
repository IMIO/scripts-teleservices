"""
This script is used to verify the setup of itsme in Authentic2.
"""

import json
import subprocess


def verify_file_exist(path):
    try:
        with open(path, "r") as file:
            return True
    except FileNotFoundError:
        return False


def verify_json_key_value(settings_json, key):
    """
    verify that


    AUTHN_CLASSREF contains more than 2 items

    Example of structure for reference :

    {
        "MELLON_IDENTITY_PROVIDERS": [
        {
            "METADATA_URL": "some_url",
            "AUTHN_CLASSREF": ["some_urn", "some_urn", "some_urn"]
        }
    ],
    }
    """
    try:
        with open(settings_json, "r") as file:
            data = json.load(file)
            if key in data:
                for element in data[key]:
                    if element["AUTHN_CLASSREF"]:
                        if len(element["AUTHN_CLASSREF"]) > 2:
                            feedback = f"OK"
                    else:
                        feedback = f"AUTHN_CLASSREF not found in {settings_json}"
            else:
                feedback = f"Key {key} not found in {settings_json}"
    except FileNotFoundError:
        feedback = f"File {settings_json} not found"

    return feedback


def verify_for_itsme():
    authentic_tenant = subprocess.run(
        "ls /var/lib/authentic2-multitenant/tenants/",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=True,
        check=True,
    )

    if authentic_tenant:
        authentic_tenant = authentic_tenant.stdout.decode("utf-8").split("\n")[0].strip()

        settings_json_path = f"/var/lib/authentic2-multitenant/tenants/{authentic_tenant}/settings.json"

        settings_json = verify_file_exist(settings_json_path)

        if not settings_json:
            error_message = (
                f"settings.json file not found in /var/lib/authentic2-multitenant/tenants/{authentic_tenant}/"
            )

        else:
            error_message = verify_json_key_value(settings_json_path, "MELLON_IDENTITY_PROVIDERS")

    return error_message + " " + settings_json_path


print(verify_for_itsme())
