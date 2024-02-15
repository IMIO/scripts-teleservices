import glob
import os

list_of_txt_files = glob.glob("*.txt")
list_of_txt_files.sort(key=os.path.getmtime)
newest = list_of_txt_files[-8:]

for el in newest:
    pos = el.find("~")
    app = el[:pos]
    old_secret = open(el, "r")
    old_secret = old_secret.read()
    old_secret = old_secret.rstrip()
    current_secret_path = f"/etc/{app}/secret"
    current_secret = open(current_secret_path, "r")
    current_secret = current_secret.read()
    current_secret = current_secret.rstrip()
    # print(f"Current {app}'s secret is: ",  f"'{current_secret}'")
    if current_secret != old_secret:
        print(f"Success! {current_secret_path} is quite different from the old one!")
    else:
        print(f"Oh no. '{current_secret_path}' is the same as the old one! Our file atleration has been lost.")
