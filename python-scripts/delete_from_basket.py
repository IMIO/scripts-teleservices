"""
Attention, supprime toutes les demandes de tous les paniers

Usage : sudo -u combo combo-manage tenant_command runscript -d ville.guichet-citoyen.be clean_baskets.py

"""

from combo.apps.lingo.models import BasketItem

BasketItem.objects.filter(payment_date__isnull=True).delete()
