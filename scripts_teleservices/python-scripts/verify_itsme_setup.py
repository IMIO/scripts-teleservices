"""
Verify the FAS (CSAM) authentication levels configured in Authentic2.

FAS reads AUTHN_CLASSREF as a minimum level and offers every authentication
mean at or above the lowest requested level, while mellon only accepts the
exact levels listed. Any level offered by FAS but missing from the list ends
with a "user not found" page, so the list must match EXPECTED_CLASSREF.
"""

import glob
import json
import os
import sys

TENANTS_GLOB = "/var/lib/authentic2-multitenant/tenants/*/settings.json"
FAS_METADATA_MARKER = "belgium.be"
EXPECTED_CLASSREF = {
    "urn:be:fedict:iam:fas:citizen:Level500",
    "urn:be:fedict:iam:fas:citizen:Level490",
    "urn:be:fedict:iam:fas:citizen:Level450",
}


def check_settings_json(settings_json_path):
    try:
        with open(settings_json_path, "r") as file:
            data = json.load(file)
    except (OSError, json.JSONDecodeError) as e:
        return f"unreadable settings.json ({e})"

    fas_idps = [
        idp
        for idp in data.get("MELLON_IDENTITY_PROVIDERS") or []
        if FAS_METADATA_MARKER in (idp.get("METADATA_URL") or "")
    ]
    if not fas_idps:
        return None

    for idp in fas_idps:
        classref = set(idp.get("AUTHN_CLASSREF") or [])
        if not classref:
            return "AUTHN_CLASSREF not found"
        if classref != EXPECTED_CLASSREF:
            missing = sorted(EXPECTED_CLASSREF - classref)
            unexpected = sorted(classref - EXPECTED_CLASSREF)
            return f"AUTHN_CLASSREF mismatch, missing: {missing}, unexpected: {unexpected}"
    return "OK"


def verify_for_itsme():
    all_ok = True
    for settings_json_path in sorted(glob.glob(TENANTS_GLOB)):
        result = check_settings_json(settings_json_path)
        if result is None:
            continue
        tenant = os.path.basename(os.path.dirname(settings_json_path))
        print(f"{tenant}: {result}")
        all_ok = all_ok and result == "OK"
    return all_ok


if __name__ == "__main__":
    sys.exit(0 if verify_for_itsme() else 1)
