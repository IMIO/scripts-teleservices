"""
Attention, supprime toutes les demandes de tous les paniers
"""

from combo.apps.lingo.models import BasketItem

BasketItem.objects.filter(payment_date__isnull=True).delete()
