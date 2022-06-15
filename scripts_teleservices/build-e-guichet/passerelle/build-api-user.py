from passerelle.base.models import ApiUser

api_user = ApiUser.objects.create(
    username='Tout_le_monde',
    fullname='Tout le monde',
    description='Tout le monde',
    keytype='',
    key=''
)

