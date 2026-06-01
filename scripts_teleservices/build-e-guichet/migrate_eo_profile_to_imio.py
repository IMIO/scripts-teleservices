# -*- coding: utf-8 -*-
"""
Migration d'un profil utilisateur authentic2 "EntreOuvert" vers le profil iMio.

Contexte
--------
Les instances historiquement gérées par EntreOuvert utilisent un profil
utilisateur réduit (typiquement un champ `address` en texte libre, sans
découpage rue/numéro/boîte). Le profil iMio (cf. hobo/recipe-commune-extra.json)
découpe l'adresse en `street`, `num_house`, `num_box`, `address_supplement`,
`zipcode`, `city`, `country`, et ajoute `phone`, `birthdate`, `niss`, `title`.

Les kinds spécialisés `street`, `num_house`, `phone`, `country`, `nrn`,
`fedict_date` sont fournis par le module `authentic2_auth_fedict` et stockent
leur valeur en JSON. Les kinds standard d'authentic2 (`string`, `title`,
`birthdate`, ...) stockent leur valeur brute. Le script s'appuie sur
`Attribute.set_value()` / `get_value()` pour que la (dé)sérialisation soit
gérée automatiquement par chaque kind.

Ce script (périmètre "adresse uniquement", cas Tournai) :
    1. exporte un dump JSON de tous les Attribute et AttributeValue concernés
       avant toute modification ;
    2. crée les 4 champs d'adresse iMio manquants (`street`, `address_supplement`,
       `num_house`, `num_box`) — aucun autre attribut existant n'est touché ;
    3. migre les valeurs des utilisateurs en parsant le contenu du champ
       `address` (regex) vers `street`, `num_house`, `num_box` et
       `address_supplement` ;
    4. désactive le seul attribut `address` une fois les valeurs migrées
       (`mobile`, `initiales`, `aes_id` et les autres champs sont conservés).

Usage
-----
    # mode simulation (par défaut) — n'écrit rien en base
    MIGRATE_DRY_RUN=1 authentic2-multitenant-manage tenant_command \
        runscript /opt/publik/scripts/scripts_teleservices/build-e-guichet/migrate_eo_profile_to_imio.py \
        -d <slug>-auth.<domain>

    # mode application réelle
    MIGRATE_DRY_RUN=0 authentic2-multitenant-manage tenant_command \
        runscript /opt/publik/scripts/scripts_teleservices/build-e-guichet/migrate_eo_profile_to_imio.py \
        -d <slug>-auth.<domain>

Variables d'environnement
-------------------------
    MIGRATE_DRY_RUN     "1" (défaut) pour simuler, "0" pour appliquer.
    MIGRATE_BACKUP_DIR  Dossier de dump JSON (défaut: /var/backups/authentic2).
"""

import json
import os
import re
import sys
from datetime import datetime

from django.contrib.contenttypes.models import ContentType
from django.db import transaction

from authentic2.models import Attribute, AttributeValue

try:
    # En production le hobo agent est installé : on enrobe la phase 2 dans
    # `with provisionning:` pour que la modification des AttributeValue
    # déclenche une re-synchronisation des utilisateurs vers wcs/combo/...
    from hobo.agent.authentic2.provisionning import provisionning
except ImportError:  # pragma: no cover — utile pour les tests hors-tenant
    provisionning = None


# --------------------------------------------------------------------------- #
# Configuration cible iMio (source: hobo/recipe-commune-extra.json)
# --------------------------------------------------------------------------- #

# Périmètre "adresse uniquement" (Tournai) : on ne crée QUE les 4 champs
# d'adresse fractionnés iMio. Aucun autre attribut existant n'est touché
# (title/first_name/zipcode/city/country/phone/birthdate/mobile/niss/initiales/
# aes_id restent intacts : ni kind, ni required, ni order modifiés).
# 'phone' et 'birthdate' restent en kind 'string' (pas de conversion).
# Ordre : les attributs existants vont de 0 à 13, donc les 4 nouveaux champs
# prennent 14-17 (affichés en bas du profil) pour ne rien décaler.
TARGET_ATTRIBUTES = [
    {
        "name": "street",
        "label": "Rue",
        "kind": "street",
        "asked_on_registration": True,
        "required": True,
        "order": 14,
    },
    {
        "name": "address_supplement",
        "label": "Complément d'adresse",
        "description": "Lieu-dit,...",
        "kind": "string",
        "asked_on_registration": True,
        "required": False,
        "order": 15,
    },
    {
        "name": "num_house",
        "label": "Numéro",
        "description": (
            "Ex. de numéro : 12, 147 et pas 1c ou 124/14. "
            "(Complément à indiquer dans le champ boite)"
        ),
        "kind": "num_house",
        "asked_on_registration": True,
        "required": True,
        "order": 16,
    },
    {
        "name": "num_box",
        "label": "Boîte",
        "kind": "string",
        "asked_on_registration": True,
        "required": False,
        "order": 17,
    },
]

# Attributs à désactiver (ne sont plus utilisés côté iMio).
ATTRIBUTES_TO_DISABLE = ["address"]

# Nom du champ source EntreOuvert dont la valeur doit être parsée vers les
# champs iMio fractionnés.
LEGACY_ADDRESS_NAME = "address"

# --------------------------------------------------------------------------- #
# Helpers
# --------------------------------------------------------------------------- #


def _env_flag(name, default="1"):
    return os.environ.get(name, default).strip().lower() in ("1", "true", "yes", "on")


DRY_RUN = _env_flag("MIGRATE_DRY_RUN", default="1")
BACKUP_DIR = os.environ.get("MIGRATE_BACKUP_DIR", "/var/backups/authentic2")


def log(msg):
    prefix = "[DRY-RUN] " if DRY_RUN else "[APPLY]  "
    print(prefix + msg)


# --------------------------------------------------------------------------- #
# Sauvegarde JSON
# --------------------------------------------------------------------------- #


def backup_state():
    """Dump tous les Attribute et leurs AttributeValue dans un fichier JSON."""
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    tenant = os.environ.get("DJANGO_SETTINGS_MODULE", "tenant")
    filename = "migrate_eo_to_imio_{}_{}.json".format(tenant, timestamp)
    path = os.path.join(BACKUP_DIR, filename)

    payload = {"attributes": [], "values": []}
    for attribute in Attribute.all_objects.all().order_by("order", "name"):
        payload["attributes"].append({
            "id": attribute.id,
            "name": attribute.name,
            "label": attribute.label,
            "description": attribute.description,
            "kind": attribute.kind,
            "required": attribute.required,
            "asked_on_registration": attribute.asked_on_registration,
            "user_editable": attribute.user_editable,
            "user_visible": attribute.user_visible,
            "disabled": attribute.disabled,
            "multiple": attribute.multiple,
            "searchable": attribute.searchable,
            "order": attribute.order,
        })
    for value in AttributeValue.objects.select_related("attribute").all():
        payload["values"].append({
            "attribute": value.attribute.name,
            "content_type_id": value.content_type_id,
            "object_id": value.object_id,
            "content": value.content,
            "multiple": value.multiple,
            "verified": value.verified,
        })

    if DRY_RUN:
        log("Sauvegarde simulée vers {} ({} attributs, {} valeurs).".format(
            path, len(payload["attributes"]), len(payload["values"])
        ))
        return None

    if not os.path.isdir(BACKUP_DIR):
        os.makedirs(BACKUP_DIR)
    with open(path, "w") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    log("Sauvegarde écrite: {} ({} attributs, {} valeurs).".format(
        path, len(payload["attributes"]), len(payload["values"])
    ))
    return path


# --------------------------------------------------------------------------- #
# Création / mise à jour / désactivation des attributs
# --------------------------------------------------------------------------- #


def upsert_attribute(spec):
    """Crée l'attribut s'il n'existe pas, ou met à jour les champs divergents."""
    name = spec["name"]
    defaults = {
        "label": spec["label"],
        "description": spec.get("description", ""),
        "kind": spec["kind"],
        "required": spec.get("required", False),
        "asked_on_registration": spec.get("asked_on_registration", False),
        "user_editable": spec.get("user_editable", True),
        "user_visible": spec.get("user_visible", True),
        "order": spec.get("order", 0),
        "disabled": False,
    }

    existing = Attribute.all_objects.filter(name=name).first()
    if existing is None:
        log("CREATE attribute name={!r} kind={!r}".format(name, spec["kind"]))
        if not DRY_RUN:
            Attribute.objects.create(name=name, **defaults)
        return

    diff = {k: v for k, v in defaults.items() if getattr(existing, k) != v}
    if not diff:
        log("OK     attribute name={!r} (no change)".format(name))
        return

    log("UPDATE attribute name={!r} diff={}".format(name, diff))
    if not DRY_RUN:
        for key, value in diff.items():
            setattr(existing, key, value)
        existing.save()


def disable_attribute(name):
    existing = Attribute.all_objects.filter(name=name).first()
    if existing is None:
        log("SKIP   disable name={!r} (does not exist)".format(name))
        return
    if existing.disabled:
        log("OK     disable name={!r} (already disabled)".format(name))
        return
    log("DISABLE attribute name={!r}".format(name))
    if not DRY_RUN:
        existing.disabled = True
        existing.save()


# --------------------------------------------------------------------------- #
# Parsing de l'adresse libre EntreOuvert
# --------------------------------------------------------------------------- #

# Mot-clé "boîte" (variantes FR/BE/EN) suivi d'un identifiant alphanumérique.
_BOX_RE = re.compile(
    r"""
    [\s,;/-]*                       # séparateur optionnel
    \b(?:bte|boite|boîte|box|bus)\b # mot-clé boîte
    \.?\s*[:.]?\s*
    (?P<num_box>[A-Za-z0-9\-\/]+)
    \s*$
    """,
    re.IGNORECASE | re.VERBOSE,
)

# Suffixe optionnel après le numéro principal : "12a", "12 bis", "12/3", "12-A".
# Sera redirigé vers num_box car NumHouseField exige des chiffres purs.
_SUFFIX = r"(?:bis|ter|quater|[A-Za-z]+|\s*[/\-]\s*\w+)"

# Numéro en TÊTE : "5 rue Royale", "2, allee des patriotes".
_NUM_HEAD_RE = re.compile(
    r"^(?P<num_house>\d+)(?P<suffix>" + _SUFFIX + r")?\s*[,;]?\s*",
    re.IGNORECASE,
)

# Numéro en QUEUE : "rue Communale 13", "Rue de la Goudinière, 32".
_NUM_TAIL_RE = re.compile(
    r"[,;]?\s*(?P<num_house>\d+)(?P<suffix>" + _SUFFIX + r")?\s*$",
    re.IGNORECASE,
)


def _clean_suffix(value):
    """Nettoie un suffixe (espaces, séparateurs) pour le stocker dans num_box."""
    if not value:
        return ""
    return re.sub(r"^[\s/\-,;]+|[\s/\-,;]+$", "", value).strip()


def parse_address(raw):
    """
    Découpe une adresse libre en (street, num_house, num_box, supplement).

    Stratégie :
      * extrait la boîte si un mot-clé bte/boîte/box est présent en fin ;
      * cherche un numéro EN TÊTE de la chaîne, sinon EN FIN. Un numéro au
        milieu n'est jamais retenu (trop incertain, ex. "rue du 8 mai 1945") ;
      * le suffixe éventuel (12a, 12bis, 12/3) part dans `num_box` car
        `NumHouseField` valide ^[1-9][0-9]*$ ;
      * en l'absence de numéro reconnaissable, toute la chaîne va dans
        `street` (l'utilisateur pourra corriger lors d'une prochaine
        connexion).
    """
    result = {
        "street": "",
        "num_house": "",
        "num_box": "",
        "address_supplement": "",
    }
    if not raw or not raw.strip():
        return result

    text = " ".join(raw.split())

    box_match = _BOX_RE.search(text)
    if box_match:
        result["num_box"] = box_match.group("num_box").strip()
        text = text[: box_match.start()].strip(" ,;/-")

    match = _NUM_HEAD_RE.match(text)
    street = ""
    if match:
        result["num_house"] = match.group("num_house")
        suffix = _clean_suffix(match.group("suffix"))
        if suffix and not result["num_box"]:
            result["num_box"] = suffix
        street = text[match.end():].strip(" ,;/-")
    else:
        match = _NUM_TAIL_RE.search(text)
        if match:
            result["num_house"] = match.group("num_house")
            suffix = _clean_suffix(match.group("suffix"))
            if suffix and not result["num_box"]:
                result["num_box"] = suffix
            street = text[: match.start()].strip(" ,;/-")
        else:
            # Aucun numéro reconnaissable : on conserve tout dans la rue.
            street = text

    result["street"] = re.sub(r"\s+", " ", street).strip()
    return result


# --------------------------------------------------------------------------- #
# Migration des valeurs utilisateur
# --------------------------------------------------------------------------- #


def _get_attr(name):
    return Attribute.all_objects.filter(name=name).first()


def _resolve_owner(content_type_id, object_id):
    """Reconstruit l'instance propriétaire (User) à partir d'un AttributeValue."""
    ct = ContentType.objects.get_for_id(content_type_id)
    return ct.get_object_for_this_type(pk=object_id)


def migrate_address_values():
    """Pour chaque AttributeValue de l'attribut legacy `address`, peuple
    street / num_house / num_box / address_supplement de l'utilisateur.

    Important : on utilise Attribute.get_value() / set_value() afin que la
    sérialisation soit correcte pour chaque kind (les kinds fedict comme
    `street` et `num_house` stockent en JSON, le kind `string` stocke brut).
    """

    legacy = _get_attr(LEGACY_ADDRESS_NAME)
    if legacy is None:
        log("SKIP   migration valeurs: aucun attribut {!r} en base.".format(LEGACY_ADDRESS_NAME))
        return

    targets = {
        name: _get_attr(name)
        for name in ("street", "num_house", "num_box", "address_supplement")
    }
    missing = [n for n, a in targets.items() if a is None]
    if missing:
        log("ABORT  migration valeurs: attributs cibles manquants {!r}".format(missing))
        return

    legacy_values = AttributeValue.objects.filter(attribute=legacy)
    total = legacy_values.count()
    log("Migration de {} valeur(s) d'adresse legacy...".format(total))

    stats = {
        "empty": 0,            # AttributeValue vide -> rien à faire
        "owner_missing": 0,    # User introuvable
        "parsed_ok": 0,        # adresse parsée avec street + num_house
        "no_num_house": 0,     # adresse parsée mais sans numéro reconnu
        "skipped_existing": 0, # cible déjà remplie pour ce champ
        "written": 0,          # set_value effectivement exécuté (apply only)
    }

    suspect_log_path = os.path.join(
        BACKUP_DIR,
        "migrate_eo_to_imio_suspects_{}.tsv".format(
            datetime.now().strftime("%Y%m%d-%H%M%S")
        ),
    )
    suspect_buffer = []  # cas sans num_house (à auditer)

    # En apply: transaction DB + provisionning hobo pour re-sync wcs/combo.
    # En dry-run: ni transaction ni provisionning (on n'écrit rien).
    if DRY_RUN or provisionning is None:
        db_cm = _NullCM()
        prov_cm = _NullCM()
    else:
        db_cm = transaction.atomic()
        prov_cm = provisionning
    with db_cm, prov_cm:
        for av in legacy_values.iterator():
            try:
                owner = _resolve_owner(av.content_type_id, av.object_id)
            except Exception as exc:
                stats["owner_missing"] += 1
                log("WARN   user_id={} introuvable ({}), skip.".format(av.object_id, exc))
                continue

            raw = legacy.get_value(owner)
            if isinstance(raw, str):
                raw = raw.strip()
            if not raw:
                stats["empty"] += 1
                continue

            parsed = parse_address(raw)
            if parsed["num_house"]:
                stats["parsed_ok"] += 1
            else:
                stats["no_num_house"] += 1
                suspect_buffer.append(
                    "{}\t{}\t{}".format(av.object_id, raw, parsed["street"])
                )

            for field_name, value in parsed.items():
                if not value:
                    continue
                attribute = targets[field_name]
                current = attribute.get_value(owner)
                if isinstance(current, str) and current.strip():
                    stats["skipped_existing"] += 1
                    continue
                if DRY_RUN:
                    continue
                attribute.set_value(owner, value)
                stats["written"] += 1

    log("--- Synthèse migration valeurs ---")
    for key, value in stats.items():
        log("  {:<18s} : {}".format(key, value))

    if suspect_buffer:
        if DRY_RUN:
            log("Suspects ({} cas sans numéro reconnu) — extrait :".format(len(suspect_buffer)))
            for line in suspect_buffer[:10]:
                log("    " + line)
            log("    ... (run en apply pour générer le fichier complet)")
        else:
            if not os.path.isdir(BACKUP_DIR):
                os.makedirs(BACKUP_DIR)
            with open(suspect_log_path, "w") as f:
                f.write("object_id\traw_address\tstreet_after_parsing\n")
                f.write("\n".join(suspect_buffer))
            log("Rapport suspects écrit: {} ({} cas)".format(
                suspect_log_path, len(suspect_buffer)
            ))


class _NullCM:
    """Context manager neutre utilisé en dry-run (pas de transaction)."""
    def __enter__(self):
        return self
    def __exit__(self, *exc):
        return False


# --------------------------------------------------------------------------- #
# Entrée principale (runscript)
# --------------------------------------------------------------------------- #


def run():
    log("=== Migration profil EntreOuvert -> iMio ===")
    log("DRY_RUN={} BACKUP_DIR={}".format(DRY_RUN, BACKUP_DIR))

    backup_state()

    log("--- Phase 1: création / mise à jour des attributs iMio ---")
    for spec in TARGET_ATTRIBUTES:
        upsert_attribute(spec)

    log("--- Phase 2: migration des valeurs d'adresse ---")
    migrate_address_values()

    log("--- Phase 3: désactivation des attributs obsolètes ---")
    for name in ATTRIBUTES_TO_DISABLE:
        disable_attribute(name)

    log("=== Terminé ({}). ===".format("simulation" if DRY_RUN else "appliqué"))


# django-extensions `runscript` cherche une fonction `run()` au niveau module.
# Lors d'un appel direct (python migrate_eo_profile_to_imio.py), on l'exécute
# aussi pour permettre les tests unitaires manuels.
if __name__ == "__main__":
    run()
    sys.exit(0)
