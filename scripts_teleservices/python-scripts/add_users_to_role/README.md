Ce script sert à créer des utilisateurs et les mettre dans un rôle.
Créer un fichier `settings.py et y ajouter les variables auth, users et role_uuid comme indiqué dans les exemples ci-dessous :
```
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

role_uuid = "uuid_du_role"
url_ts = "https://canary-auth.guichet-citoyen.be/"

```