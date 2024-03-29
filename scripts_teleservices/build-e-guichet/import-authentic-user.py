"""
Legacy script, not used anymore.
"""

import hashlib

from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django_rbac.utils import get_ou_model, get_role_model
from hobo.agent.authentic2.provisionning import provisionning


def create_authentic_user():
    User = get_user_model()
    OU = get_ou_model()
    Role = get_role_model()
    organisation_unit = OU.objects.get(default=True)
    with provisionning:
        # create default role in ts2.
        try:
            role_agent_fabriques = Role.objects.get(name="Agent ayant acces aux fabriques")
        except ObjectDoesNotExist:
            role_agent_fabriques = Role(name="Agent ayant acces aux fabriques", ou=organisation_unit)
            role_agent_fabriques.save()

        try:
            role_agent_traitant_pop = Role.objects.get(name="Agents traitants - Population, etat civil")
        except ObjectDoesNotExist:
            role_agent_traitant_pop = Role(name="Agents traitants - Population, etat civil", ou=organisation_unit)
            role_agent_traitant_pop.save()

        try:
            role_agent_traitant_trav = Role.objects.get(name="Agents traitants - Travaux")
        except ObjectDoesNotExist:
            role_agent_traitant_trav = Role(name="Agents traitants - Travaux", ou=organisation_unit)
            role_agent_traitant_trav.save()

        try:
            role_citoyen_test = Role.objects.get(name="Citoyen (test)")
        except ObjectDoesNotExist:
            role_citoyen_test = Role(name="Citoyen (test)", ou=organisation_unit)
            role_citoyen_test.save()

        try:
            role_debug = Role.objects.get(name="Debug")
        except ObjectDoesNotExist:
            print

        with open("/tmp/tmp_uuid_agent_fabriques.txt", "w") as f:
            f.write(role_agent_fabriques.uuid)
            f.close()

        with open("/tmp/tmp_uuid_agent_traitant_pop.txt", "w") as f:
            f.write(role_agent_traitant_pop.uuid)
            f.close()

        with open("/tmp/tmp_uuid_agent_traitant_trav.txt", "w") as f:
            f.write(role_agent_traitant_trav.uuid)
            f.close()

        with open("/tmp/tmp_uuid_citoyen_test.txt", "w") as f:
            f.write(role_citoyen_test.uuid)
            f.close()

        with open("/tmp/tmp_uuid_debug.txt", "w") as f:
            f.write(role_debug.uuid)
            f.close()

        user_admin = User.objects.get(username="admin")
        role_debug.members.add(user_admin)


def create_password(commune_id):
    m = hashlib.md5(commune_id)
    return m.hexdigest()


create_authentic_user()
