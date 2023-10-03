"""This will install the tenant settings file for the tenant with the given slug."""

import argparse
import json
import os


def main(slug, domain):
    """Install the tenant settings file for the tenant with the given slug."""
    verify_arg(slug)
    filename = "settings.json"
    save_path = f"/var/lib/authentic2-multitenant/tenants/{slug}-auth.{domain}/"
    absolute_filename = save_path + filename
    python_dict = load_and_modify_json(slug)

    try:
        validate_file_access(absolute_filename)
        write_to_file(absolute_filename, python_dict)
    except (FileNotFoundError, PermissionError, IOError) as exc:
        raise


def verify_arg(arg):
    """Verify that arg exist and is a slug."""
    if arg is None:
        raise ValueError("No slug provided")
    if not arg.islower():
        raise ValueError(f"Slug {arg} is not lowercase")
    if not arg.isalnum():
        raise ValueError(f"Slug {arg} is not alphanumeric")


def load_and_modify_json(slug):
    """Load the json file and modify the values for the given slug."""
    json_string = """
    {
    "THEME_SKELETON_URL": "https://communeSlug.guichet-citoyen.be/__skeleton__/",
    "A2_AUTH_SAML_ENABLE": false,
    "A2_EMAIL_IS_UNIQUE": true,
    "A2_AUTH_FEDICT_ENABLE": true,
    "A2_PROFILE_DISPLAY_EMPTY_FIELDS": true,
    "A2_NUMHOUSE_ERROR_MESSAGE": "Rentrez un format valide. Ex. de numéro : 12, 147 et pas 1c ou 124/14. (Complément à indiquer dans le champ boite)",
    "A2_OPENED_SESSION_COOKIE_DOMAIN": "parent",
    "MELLON_ADAPTER": ["authentic2_auth_fedict.adapters.AuthenticAdapter"],
    "MELLON_LOGIN_URL": "fedict-login",
    "MELLON_PUBLIC_KEYS": [
        "/var/lib/authentic2-multitenant/tenants/communeSlug-auth.guichet-citoyen.be/saml.crt"
    ],
    "MELLON_PRIVATE_KEY": "/var/lib/authentic2-multitenant/tenants/communeSlug-auth.guichet-citoyen.be/saml.key",
    "MELLON_IDENTITY_PROVIDERS": [
        {
        "METADATA_URL": "https://iamapps-public.belgium.be/saml/fas-metadata.xml",
        "AUTHN_CLASSREF": [
            "urn:be:fedict:iam:fas:citizen:eid",
            "urn:be:fedict:iam:fas:citizen:token",
            "urn:be:fedict:iam:fas:citizen:bmid"
        ]
        }
    ],
    "MELLON_ATTRIBUTE_MAPPING": {
        "last_name": "{attributes[surname][0]}",
        "first_name": "{attributes[givenName][0]}"
    },
    "A2_USERNAME_LABEL": "Adresse e-mail",
    "A2_AUTH_OIDC_ENABLE": false,
    "A2_FC_ENABLE": false
    }
    """

    python_dict = json.loads(json_string)

    python_dict["THEME_SKELETON_URL"] = python_dict["THEME_SKELETON_URL"].replace(
        "communeSlug", slug
    )
    python_dict["MELLON_PUBLIC_KEYS"][0] = python_dict["MELLON_PUBLIC_KEYS"][0].replace(
        "communeSlug", slug
    )
    python_dict["MELLON_PRIVATE_KEY"] = python_dict["MELLON_PRIVATE_KEY"].replace(
        "communeSlug", slug
    )

    return python_dict


def validate_file_access(absolute_filename):
    """Validate that the file exists and is writable. If not, raise an exception."""
    if os.path.exists(absolute_filename):
        if not os.access(absolute_filename, os.W_OK):
            raise PermissionError("File is not writable")

    else:
        try:
            open(absolute_filename, "w").close()
        except IOError:
            raise IOError("File is not writable")


def write_to_file(absolute_filename, python_dict):
    """Write the python dict to the file."""
    with open(absolute_filename, "w", encoding="utf-8") as file:
        json.dump(python_dict, file, indent=4, ensure_ascii=False)
        print(f"Successfully written {absolute_filename}.")
        file.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Install the tenant settings file for the tenant with the given slug."
    )
    parser.add_argument("slug", help="The slug of the tenant (e.g. namur)")
    parser.add_argument(
        "domain", help="The domain of the tenant (e.g. guichet-citoyen.be)"
    )
    args = parser.parse_args()
    main(args.slug, args.domain)
