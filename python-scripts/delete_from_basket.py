# delete-from-basket.py
import sys

from combo.apps.lingo.models import BasketItem
from combo.apps.lingo.models import timezone

if __name__ == "__main__":
    print(len(sys.argv))
    len_argv = len(sys.argv)
    usage = "Usage : python delete-from-basket.py <unique/multiple> slug/id\nExamples :\npython delete-from-basket.py unique changement-d-adresse/16\npython delete-from-basket.py multiple extrait-casier-judiciaire/32"
    if len_argv > 3:
        print("Please no more than 2 arguments needed to run this script!")
    elif len_argv == 1:
        print(print(usage))
    elif len_argv == 2:
        print("It seems an argument is missing...")
        print(usage)
    elif len_argv == 3:
        if sys.argv[1] == "unique":
            print("unique mode")
            item = BasketItem.objects.get(source_url__endswith=sys.argv[2])
            item.cancellation_date = timezone.now()
            item.save()
        elif sys.argv[1] == "multiple":
            print("multiple mode")
            items = BasketItem.objects.filter(source_url__endswith=sys.argv[2])
            for item in items:
                item.cancellation_date = timezone.now()
                item.save()
