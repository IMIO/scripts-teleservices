from django.core.management.utils import get_random_secret_key

apps = ["chrono", "fargo", "passerelle", "authentic2-multitenant", "combo", "wcs", "bijoe", "hobo"]
for el in apps:
    secret_path = f"/etc/{el}/secret"
    print(secret_path)
    try:
        secret = open(secret_path, "r")
        secret = secret.read()
        secret = secret.rstrip()
        print(f"Current {el}'s secret is '{secret}'")
    except:
        print(f"I encountered a problam accessing '{secret_path}'")
    try:
        new_randomly_generated_secret = get_random_secret_key()
        secret = open(secret_path, "w")
        secret.write(new_randomly_generated_secret)
        print(f"Success! I just updated {el}'s secret!")
    except:
        print(f"Oh no. I didn't updated the {el}'s secret...")
