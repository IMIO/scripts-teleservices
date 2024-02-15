THEME_SKELETON_URL = "https://nomcommune.guichet-citoyen.be/__skeleton__/"
A2_AUTH_SAML_ENABLE = False
A2_EMAIL_IS_UNIQUE = True
A2_AUTH_FEDICT_ENABLE = True
A2_PROFILE_DISPLAY_EMPTY_FIELDS = True
A2_NUMHOUSE_ERROR_MESSAGE = "Rentrez un format valide. Ex. de num\u00e9ro : 12, 147 et pas 1c ou 124/14. (Compl\u00e9ment \u00E0 indiquer dans le champ bo\u00EEte)"
A2_OPENED_SESSION_COOKIE_DOMAIN = "parent"
MELLON_ADAPTER = ["authentic2_auth_fedict.adapters.AuthenticAdapter"]
MELLON_LOGIN_URL = "fedict-login"
MELLON_PUBLIC_KEYS = ["/var/lib/authentic2-multitenant/tenants/nomcommune-auth.guichet-citoyen.be/saml.crt"]
MELLON_PRIVATE_KEY = "/var/lib/authentic2-multitenant/tenants/nomcommune-auth.guichet-citoyen.be/saml.key"
MELLON_IDENTITY_PROVIDERS = [
    {
        "METADATA_URL": "https://iamapps-public.belgium.be/saml/fas-metadata.xml",
        "AUTHN_CLASSREF": [
            "urn:be:fedict:iam:fas:citizen:eid",
            "urn:be:fedict:iam:fas:citizen:token",
            "urn:be:fedict:iam:fas:citizen:bmid",
        ],
    }
]
MELLON_ATTRIBUTE_MAPPING = {
    "last_name": "{attributes[surname][0]}",
    "first_name": "{attributes[givenName][0]}",
}

A2_USERNAME_LABEL = "Adresse e-mail"
