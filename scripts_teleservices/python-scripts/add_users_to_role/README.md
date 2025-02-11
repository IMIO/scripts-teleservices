Ce script sert à créer des utilisateurs et les mettre dans un rôle.
Créer un fichier `settings.py et y ajouter les variables auth, users et role_uuid comme indiqué dans les exemples ci-dessous :
``` python
auth = ("login", "password")

users = [
    {
        "first_name": "Jean",
        "last_name": "Dupont",
        "email": "jean.dupont@imio.be",
        "username": "jdupont",
        "send_registration_email": True,
    }
]


url_ts = "https://canary-auth.guichet-citoyen.be/"
# identifiant court des rôles dans lesquels ajouter des users
slugs = [
    "agent-imio-portail-parents","schlagvuk"
]
url_role = f"{url_ts}api/roles/?slug="
```

