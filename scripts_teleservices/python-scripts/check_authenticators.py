"""
20230929 - Script to have a global perspective of the authenticators and their
slugs

Example of usage:

    sudo -u authentic-multitenant authentic2-multitenant-manage \
        tenant_command runscript -d staging-auth.guichet-citoyen.be \
        [path_to_script.py]
"""
import subprocess

from authentic2.apps.authenticators.models import BaseAuthenticator

tenant = subprocess.run(
    "ls /var/lib/authentic2-multitenant/tenants/",
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    shell=True,
    check=True,
)

if tenant:
    tenant = tenant.stdout.decode("utf-8").strip()

    for authenticator in BaseAuthenticator.objects.filter(enabled=True):
        log_iter_string = f"{tenant} : {authenticator.slug} {authenticator.name}"
        print(log_iter_string)
