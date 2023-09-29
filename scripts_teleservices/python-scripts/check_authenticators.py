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
    tenant = tenant.stdout.decode("utf-8").split("\n")[0].strip()

    # filter activated authenticators only :
    # BaseAuthenticator.objects.filter(enabled=True)
    for authenticator in BaseAuthenticator.objects.all():
        log_iter_string = f"{tenant} : Slug: {authenticator.slug} · Name: {authenticator.name or 'None'} · Enadled: {authenticator.enabled}"
        print(log_iter_string)
