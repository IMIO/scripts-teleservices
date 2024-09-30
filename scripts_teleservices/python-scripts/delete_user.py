from django.contrib.auth import get_user_model

User = get_user_model()
admin_to_delete = User.objects.get(username='admin_commune')
print(admin_to_delete)
admin_to_delete.delete()