from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist

User = get_user_model()

try:
    admin_to_delete = User.objects.get(username='admin_commune')
    print(admin_to_delete)
    admin_to_delete.delete()
except ObjectDoesNotExist:
    print("L'utilisateur 'admin_commune' n'existe pas.")
