# usage : sudo -u hobo hobo-manage tenant_command runscript -d demo-hobo.guichet-citoyen.be /opt/publik/scripts/scripts_teleservices/build-e-guichet/hobo_create_variables.py

from hobo.environment.models import Variable


def create_variable(name, label, value):
    variable, created = Variable.objects.get_or_create(
        name=name, defaults={"label": label, "value": value}
    )
    if created:
        print(f"Variable '{name}' has been created.")
    else:
        print(f"Variable '{name}' already exists. Fine.")


create_variable(
    "commune_name", "Nom de la commune", "Publik local iA.Téléservices dmuyshond"
)
create_variable(
    "commune_slug",
    "Nom de la commune sans accent, sans espace (mettre des tirets), en minuscule.",
    "Isnes",
)
create_variable("commune_cp", "Code postal/postaux de la commune", "5032")
create_variable(
    "administration_adresse",
    "Adresse complète de l'administration",
    "1, Rue Léon Morel - 5032 Isnes",
)
create_variable(
    "administration_site", "Site Internet de la commune", "https://www.imio.be"
)
create_variable(
    "global_title",
    "Intitulé de l'instance et mails",
    "Publik local iA.Téléservices dmuyshond",
)
create_variable("organisme", "Type d'organisme", "commune de")
