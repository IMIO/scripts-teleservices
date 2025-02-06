from settings import auth, users, url_ts, slugs, url_role
import requests

ENDPOINT_USERS = "api/users/"

headers = {"Content-Type":"application/json"}
user_uuid_dict = {"data": []}

for user in users:
    print(f"Essaie {user['email']}")
    get_user_request = requests.get(f"{url_ts}{ENDPOINT_USERS}?email={user['email']}", auth=auth, headers=headers)
    if get_user_request.json()['results']:
        print("..L'utilisateur a été trouvé")
        uuid_dict = {"uuid": get_user_request.json()['results'][0]['uuid']}
    else:
        print("..Création de l'utilisateur")
        create_user_request = requests.post(f"{url_ts}{ENDPOINT_USERS}", auth=auth, headers=headers, json=user)
        uuid_dict = {"uuid": create_user_request.json()['uuid']}
    user_uuid_dict['data'].append(uuid_dict)
print(f"Ajout du rôle à {len(user_uuid_dict['data'])} utilisateurs")
for slug in slugs:
    get_role_uuid_request = requests.get(f"{url_role}{slug}", auth=auth, headers=headers)
    if get_role_uuid_request.json()['results']:
        print("..Le rôle a été trouvé")
        role_uuid = get_role_uuid_request.json()['results'][0]['uuid']
        add_user_roles_request = requests.post(f"{url_ts}api/roles/{role_uuid}/relationships/members/", auth=auth, headers=headers, json=user_uuid_dict)
        print(f"..Création du rôle :  {add_user_roles_request.status_code}")
    else:
        print("..Le rôle n'a pas été trouvé, abandon")
#print(add_user_role_request.json())
