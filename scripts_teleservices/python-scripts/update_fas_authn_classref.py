"""
Set the FAS (CSAM) AUTHN_CLASSREF of every Authentic2 tenant to the expected levels.

FAS reads AUTHN_CLASSREF as a minimum level and offers every authentication
mean at or above the lowest requested level, while mellon only accepts the
exact levels listed. Any level offered by FAS but missing from the list ends
with a "user not found" page (SUP-57721).

Meant to be run as root on every instance (e.g. through Rundeck):

    python3 update_fas_authn_classref.py            # dry run, writes nothing
    python3 update_fas_authn_classref.py --apply    # writes, with a timestamped backup

hobo reloads settings.json as soon as its mtime changes, no restart is needed.
Keep EXPECTED_CLASSREF in sync with verify_itsme_setup.py and
build-e-guichet/install_authentic2_tenant_settings_json.py.
"""

import argparse
import datetime
import glob
import json
import os
import shutil
import socket
import sys
import tempfile

TENANTS_GLOB = "/var/lib/authentic2-multitenant/tenants/*/settings.json"
FAS_METADATA_MARKER = "belgium.be"
EXPECTED_CLASSREF = [
    "urn:be:fedict:iam:fas:citizen:Level500",
    "urn:be:fedict:iam:fas:citizen:Level490",
    "urn:be:fedict:iam:fas:citizen:Level450",
]


def find_fas_idps(content):
    return [
        idp
        for idp in content.get("MELLON_IDENTITY_PROVIDERS") or []
        if FAS_METADATA_MARKER in (idp.get("METADATA_URL") or "")
    ]


def write_atomically(path, content):
    stat = os.stat(path)
    fd, tmp_path = tempfile.mkstemp(dir=os.path.dirname(path), prefix=".settings.json.")
    try:
        with os.fdopen(fd, "w") as file:
            json.dump(content, file, indent=4, ensure_ascii=False)
            file.write("\n")
        os.chmod(tmp_path, stat.st_mode & 0o7777)
        os.chown(tmp_path, stat.st_uid, stat.st_gid)
        os.replace(tmp_path, path)
    except BaseException:
        os.unlink(tmp_path)
        raise


def process(settings_json_path, apply):
    tenant = os.path.basename(os.path.dirname(settings_json_path))
    # settings.json may be a symlink: update its target, never replace the link
    real_path = os.path.realpath(settings_json_path)
    try:
        with open(real_path) as file:
            content = json.load(file)
    except (OSError, json.JSONDecodeError) as e:
        print(f"{tenant}: ERROR unreadable settings.json ({e})")
        return False

    fas_idps = find_fas_idps(content)
    if not fas_idps:
        return True
    if all(idp.get("AUTHN_CLASSREF") == EXPECTED_CLASSREF for idp in fas_idps):
        print(f"{tenant}: up to date")
        return True

    for idp in fas_idps:
        print(f"{tenant}: {idp.get('AUTHN_CLASSREF')} -> {EXPECTED_CLASSREF}")
        idp["AUTHN_CLASSREF"] = list(EXPECTED_CLASSREF)
    if apply:
        backup_path = "%s.bak-%s" % (real_path, datetime.datetime.now().strftime("%Y%m%d-%H%M%S"))
        shutil.copy2(real_path, backup_path)
        write_atomically(real_path, content)
        print(f"{tenant}: updated (backup: {backup_path})")
    return True


def main():
    parser = argparse.ArgumentParser(description=__doc__.strip().splitlines()[0])
    parser.add_argument("--apply", action="store_true", help="write the changes")
    args = parser.parse_args()

    print(f"host: {socket.gethostname()}")
    paths = sorted(glob.glob(TENANTS_GLOB))
    if not paths:
        print(f"no file matches {TENANTS_GLOB}")
        return 1
    all_ok = True
    for settings_json_path in paths:
        all_ok = process(settings_json_path, args.apply) and all_ok
    if not args.apply:
        print("dry run: nothing written, use --apply to write the changes")
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
