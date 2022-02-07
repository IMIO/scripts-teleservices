import datetime
import glob
import os

now = datetime.datetime.now()

apps = ['chrono', 'fargo', 'passerelle', 'authentic2-multitenant', 'combo', 'wcs', 'bijoe', 'hobo']
cwd = os.getcwd()
for el in apps:
    fhand = open(f'/etc/{el}/secret')
    secret = fhand.read()
    secret = secret.rstrip()
    filename = f'{el}~old_secret_{now.year}{now.month}{now.day}.txt'
    fhand_save_secret = open(f'{cwd}/{filename}', 'w')
    fhand_save_secret.write(f'{secret}')
    fhand_save_secret = open(f'{cwd}/{filename}', 'r')
    saved_secret = fhand_save_secret.read()
    saved_secret = saved_secret.rstrip()
    print(f"I saved {el}'s secret which currently is: ", f"'{saved_secret}'", f"in {cwd}/{filename}")

