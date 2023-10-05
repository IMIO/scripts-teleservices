"""
20230411 · See:
https://dev.entrouvert.org/issues/81462#note-11

Le script générera une requête SQL à chaque itération de la boucle, soit 1000 requêtes
en total.

User.objects.all()[:1] génère une requête SQL qui cherche le premier utilisateur dans
la base de données.

Le script mesure le temps écoulé entre chaque itération, ce qui peut aider à identifier
des problèmes de performance.

Si le temps d'exécution augmente de manière significative pendant les périodes de trafic
élevé, cela peut indiquer un problème au niveau de la base de données PostgreSQL.

Par contre, si le temps d'exécution reste constant, le problème pourrait être ailleurs.

Usage:

sudo -u authentic-multitenant authentic2-multitenant-manage tenant_command \
    runscript -d \
    mettet-auth.guichet-citoyen.be \
    /opt/publik/scripts/scripts_teleservices/python-scripts/generate_1000_SQL_requests.py


"""

from django.contrib.auth import get_user_model

User = get_user_model()

import time

t0 = time.time()

for i in range(1000):
    print(i + 1, time.time() - t0)
    User.objects.all()[:1]  # any sql query
