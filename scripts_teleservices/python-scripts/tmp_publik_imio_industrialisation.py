"""
This is used as a temporary monkey-patch using rundeck following #83567
"""

import json
import os
import random
import subprocess
import tempfile
import time
import urllib.parse

from django.core.management.base import BaseCommand
from django.db import connection
from django.template import Context, Template
from hobo.agent.worker import settings as agent_settings
from hobo.environment.models import Authentic, Combo, Passerelle, Wcs
from hobo.multitenant.management.commands import InteractiveTenantOption


class Command(InteractiveTenantOption, BaseCommand):
    def add_arguments(self, parser):
        super().add_arguments(parser)
        parser.add_argument('--directory', dest='directory')

    def handle(self, *args, **options):
        agent_settings.WCS_MANAGE_COMMAND = 'sudo -u wcs /usr/bin/wcsctl -f /etc/wcs/wcs.cfg'
        tenant = self.get_tenant_from_options_or_interactive(**options)
        connection.set_tenant(tenant)
        self.directory = options['directory']

        self.authentic = Authentic.objects.all().first()
        self.combos = list(Combo.objects.filter(secondary=False))
        self.passerelle = Passerelle.objects.filter(secondary=False).first()
        self.wcs = Wcs.objects.filter(secondary=False).first()

        for service in [self.authentic, self.passerelle, self.wcs] + self.combos:
            service.tenant_name = urllib.parse.urlparse(service.base_url).netloc

        self.env = {k: v for k, v in os.environ.items() if k.endswith('_SETTINGS_FILE')}
        if not self.wait_for_roles(nowait=True):
            self.import_roles()
            self.wait_for_roles()
        self.import_wcs()
        self.import_combos()
        self.import_passerelle()

    def get_templated_file(self, template_name):
        with open(template_name) as fd:
            first_line = fd.readline()
            if '{#' in first_line:
                # template marker
                fd.seek(0)
                template = Template(fd.read())
                context = Context({'environ': os.environ})
                new_file_name = os.path.join(
                    tempfile.gettempdir(), '%s-%s' % (tempfile.gettempprefix(), random.randint(0, 10**10))
                )
                with open(new_file_name, 'w') as fd2:
                    fd2.write(template.render(context))
                return new_file_name
        return template_name

    def import_roles(self):
        roles_filename = os.path.join(self.directory, 'roles/roles.json')
        if not os.path.exists(roles_filename):
            return
        cmd = agent_settings.AUTHENTIC_MANAGE_COMMAND.split()
        subprocess.run(
            cmd
            + [
                'tenant_command',
                'import_site',
                '-d',
                urllib.parse.urlparse(self.authentic.base_url).netloc,
                self.get_templated_file(roles_filename),
            ],
            env=self.env,
        )

    def wait_for_success(self, cmd, nowait=False):
        while True:
            process = subprocess.run(cmd, env=self.env)
            if process.returncode == 0 or nowait:
                return process.returncode
            time.sleep(0.5)

    def wait_for_roles(self, nowait=False):
        roles_filename = os.path.join(self.directory, 'roles/roles.json')
        if not os.path.exists(roles_filename):
            return
        wcs_cmd = agent_settings.WCS_MANAGE_COMMAND.split()
        combo_cmd = agent_settings.COMBO_MANAGE_COMMAND.split()
        roles = json.load(open(self.get_templated_file(roles_filename)))
        rc = 0
        for role in roles['roles']:
            role_name = role['name']
            rc += self.wait_for_success(
                wcs_cmd + ['has_role', '-d', self.wcs.tenant_name, role_name], nowait=nowait
            )
            for combo in self.combos:
                rc += self.wait_for_success(
                    combo_cmd + ['tenant_command', 'has_role', '-d', combo.tenant_name, role_name],
                    nowait=nowait,
                )
            if rc and nowait:
                break
        return bool(rc == 0)

    def import_wcs(self):
        wcs_cmd = agent_settings.WCS_MANAGE_COMMAND.split()
        cmd = wcs_cmd + ['imio_import_directory', '-d', self.wcs.tenant_name, self.directory]
        subprocess.run(cmd, env=self.env)

    def import_combos(self):
        combo_cmd = agent_settings.COMBO_MANAGE_COMMAND.split()
        for combo in self.combos:
            exported_file = os.path.join(self.directory, 'combo/%s.json' % combo.template_name)
            if not os.path.exists(exported_file):
                continue
            cmd = combo_cmd + [
                'tenant_command',
                'import_site',
                '-d',
                combo.tenant_name,
                self.get_templated_file(exported_file),
            ]
            subprocess.run(cmd, env=self.env)

    def import_passerelle(self):
        if not os.path.exists(os.path.join(self.directory, 'passerelle')):
            return
        passerelle_cmd = agent_settings.PASSERELLE_MANAGE_COMMAND.split()
        for filename in os.listdir(os.path.join(self.directory, 'passerelle')):
            if not filename.endswith('.json'):
                continue
            exported_file = os.path.join(self.directory, 'passerelle', filename)
            cmd = passerelle_cmd + [
                'tenant_command',
                'import_site',
                '-d',
                self.passerelle.tenant_name,
                self.get_templated_file(exported_file),
            ]
            subprocess.run(cmd, env=self.env)