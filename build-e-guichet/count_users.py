# -*- coding: utf-8 -*-
# authentic2-multitenant-manage tenant_command runscript /opt/publik/scripts/build-e-guichet/cpt_auth_users.py -d lalouviere-auth.guichet-citoyen.be

from datetime import date,timedelta
from django.contrib.auth import get_user_model
import json 

def ct_all_users():
    return User.objects.all().count()


def cpt_users_with_rights():
    return User.objects.filter(roles__isnull=False).distinct().count()


def cpt_users_with_recent_connexion(days=90):
    today = date.today()
    last_login_limit = today - timedelta(days=days)
    return User.objects.filter(last_login__range=(last_login_limit, today)).count()


def cpt_all_users():
    return User.objects.all().count()


def cpt_users_with_rights():
    return User.objects.filter(roles__isnull=False).distinct().count()


def cpt_users_with_recent_connexion(days=90):
    today = date.today()
    last_login_limit = today - timedelta(days=days)
    return User.objects.filter(last_login__range=(last_login_limit, today)).count()


User = get_user_model()
cpt_all_users = cpt_all_users()
cpt_users_with_rights = cpt_users_with_rights()
cpt_users_with_recent_connexion = cpt_users_with_recent_connexion()
print (json.dumps({
    'all_users': cpt_all_users,
    'users_with_rights': cpt_users_with_rights,
    'users_with_recent_connexion': cpt_users_with_recent_connexion
}))
