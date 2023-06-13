# authentic2-multitenant-manage tenant_command runscript /opt/publik/scripts/scripts_teleservices/build-e-guichet/auth_fedict_var.py -d $1-auth.$2
# For reference or as documentation, here is the initial commit message related to this whole script : "Adapt script to have list of countries instead of plain text"
from authentic2.models import Attribute

try:
    Attribute.objects.filter(name="country").update(kind="country")
except Exception as e:
    # log the exception
    print(
        f"❌ An error occurred while running  authentic2-multitenant-manage tenant_command runscript /opt/publik/scripts/scripts_teleservices/build-e-guichet/auth_fedict_var.py : {e}"
    )
