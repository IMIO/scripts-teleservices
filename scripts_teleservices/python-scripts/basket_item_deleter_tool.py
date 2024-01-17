"""
This script is used to delete BasketItem objects from the database.

It is useful when you want to delete BasketItem objects that is not possible to
delete otherwise (e.g following a bug).

To use it, you need to provide the email of the user whose BasketItem objects
you want to delete. The script will then print the details of the BasketItem
objects related to the user and ask if you want to delete one of them.

If you want to delete an item, you need to provide its id.

Example usage:

sudo -u combo combo-manage tenant_command runscript -d olln.guichet-citoyen.be /opt/publik/scripts/scripts_teleservices/python-scripts/debug_basket.py

"""

# Import the necessary models
from combo.apps.lingo.models import BasketItem, timezone
from django.contrib.auth.models import User

item = BasketItem.objects.first()


# print(type(item.user))
# print(item.user)

# Ask user for email and trim input
user_email = input("Enter the email of the user whose basket items you want to delete: ")
user_email = user_email.strip()

# Verify email validity using regex
import re

email_regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"

if not re.match(email_regex, user_email):
    print("Invalid email provided. Exiting...")
    exit()


# Function to print the details of BasketItem objects for a given user email
def print_user_basket_items(user_email):
    try:
        # First, get the User object by email
        user = User.objects.get(email=user_email)
    except User.DoesNotExist:
        print(f"User not found with email: {user_email}")
        return

    # Fetching BasketItem objects related to the user
    basket_items = BasketItem.objects.filter(user=user)

    if basket_items:
        print(f"\n\n\nBasket Items for {user_email}:\n\n\n")
        for item in basket_items:
            print(
                f" ----\n id: {item.id},\n subject: {item.subject},\n details: {item.details},\n amount: {item.amount},\n extra_fee: {item.extra_fee},\n creation_date: {item.creation_date},\n source_url: {item.source_url},\n payment_url: {item.payment_url},\n regie: {item.regie},"
            )
    else:
        print(f"No basket items found for {user_email}")


# Retrieve BasketItem objects for the user
print_user_basket_items(user_email)


# Ask if user wants to delete an item
want_to_delete = input("\n\n\nDo you want to delete an item? (y/n): ")

if want_to_delete.lower() != "y":
    exit()

# Ask for the id of the item to delete
id_of_element_to_delete = input("\nEnter the id of the item to delete: ")

if not id_of_element_to_delete:
    print("No id provided. Exiting...")
    exit()

# Verify id validity
try:
    id_of_element_to_delete = int(id_of_element_to_delete)
except ValueError:
    print("Invalid id provided. Exiting...")
    exit()

item = BasketItem.objects.get(id=id_of_element_to_delete)

if item:
    print(
        f"\n\n\nDeleting following item :\n\n\n id: {id_of_element_to_delete},\n subject: {item.subject},\n details: {item.details},\n amount: {item.amount},\n extra_fee: {item.extra_fee},\n creation_date: {item.creation_date},\n source_url: {item.source_url},\n payment_url: {item.payment_url},\n regie: {item.regie},"
    )
    input("Press Enter to delete the item")
    item.cancellation_date = timezone.now()
    item.save()
    print("Item deleted successfully")
else:
    print(f"No item found with id {id_of_element_to_delete}")
