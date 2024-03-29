# sudo -u combo combo-manage tenant_command runscript -d local.example.net lingo_create_regie.py
import eopayment
from combo.apps.lingo.models import PaymentBackend, Regie

service_opt = {
    "payment_means": "VISA,MASTERCARD,MAESTRO",
    "platform": "test",
    "secret_key": "002001000000001_KEY1",
    "merchant_id": "002001000000001",
    "key_version": "1",
}

pb, paybackend_created = PaymentBackend.objects.get_or_create(
    label="Atos test",
    slug="atos_test",
    defaults={
        "service": eopayment.SIPS2,
        "service_options": service_opt,
    },
)

try:
    Regie(
        label="Atos test",
        slug="atos_test",
        description="Atos test",
        text_on_success="Votre paiement a été pris en compte. Si votre demande est validée par nos services, vous recevrez très prochainement votre document par voie postale. Si votre demande n'est pas valide, vous serez prévenu par e-mail et remboursé de la somme perçue dans les meilleurs délais",
        payment_backend=pb,
        is_default=True,
    ).save()
    regie_created = True
except:
    regie_created = False
    pass  # This custom Entr'Ouvert class does not allow something similar to get_or_create()


#      extra_fees_ws_url="https://{}-passerelle.{}/extra-fees/calcul-des-frais-de-port/compute".format(sys.argv[1],sys.argv[2]),

if paybackend_created:
    print(f"PaymentBackend '{pb.label}' has been created.")
else:
    print(f"PaymentBackend '{pb.label}' already exists. Fine.")

if regie_created:
    print(f"Regie 'Atos test' has been created.")
else:
    print(
        f"Regie 'Atos test' creation failed (Regie().save() failed). It might simply already exist. Regie() class does not allow get_or_create() so we can't check for sure here. It might be a good idea to check manually that it effectively exists. If you want more info about this, read lingo_create_regie.py."
    )
