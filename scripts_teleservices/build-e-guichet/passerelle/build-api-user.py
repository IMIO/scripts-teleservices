from passerelle.base.models import ApiUser

api_user, created = ApiUser.objects.get_or_create(
    username="Tout_le_monde",
    defaults={
        "fullname": "Tout le monde",
        "description": "Tout le monde",
        "keytype": "",
        "key": "",
    },
)

if created:
    print(f"api_user '{api_user.username}' has been created.")
else:
    print(f"api_user '{api_user.username}' already exists. Fine.")
