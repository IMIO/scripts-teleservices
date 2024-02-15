"""
Will generate a 1liner that will test our db with psql cmd.
Asked by the infra team.
"""
import re


def main():
    # Usage:
    database, user, password, host, port = get_psql_cmd_details()

    cmd_prefix = f"for i in {{1..1000}}; do PGPASSWORD={password} psql -h {host}"
    cmd_suffix = (
        f' -p {port} -d {database} -U {user} -c "SET SCHEMA '
        "'mettet_auth_guichet_citoyen_be'; "
        "EXPLAIN ANALYZE VERBOSE "
        "SELECT id, password, last_login, uuid, username, first_name, "
        "last_name, email, email_verified, email_verified_date, "
        "email_verified_sources, is_superuser, phone, phone_verified_on, "
        "is_staff, is_active, ou_id, date_joined, modified, "
        "last_account_deletion_alert, deactivation, deactivation_reason, "
        "keepalive FROM custom_user_user ORDER BY last_name ASC, "
        'first_name ASC, email ASC, username ASC LIMIT 1;"; done'
    )

    cmd = f"{cmd_prefix}{cmd_suffix}"
    print(cmd)


def get_psql_cmd_details():
    with open("/etc/authentic2-multitenant/settings.d/config.py", "r") as file:
        content = file.read()

        database_name = re.search(r"DATABASES\['default'\]\['NAME'\] = '(.+?)'", content).group(1)
        user = re.search(r"DATABASES\['default'\]\['USER'\] = '(.+?)'", content).group(1)
        password = re.search(r"DATABASES\['default'\]\['PASSWORD'\] = '(.+?)'", content).group(1)
        host = re.search(r"DATABASES\['default'\]\['HOST'\] = '(.+?)'", content).group(1)
        port = re.search(r"DATABASES\['default'\]\['PORT'\] = '(.+?)'", content).group(1)

    return (database_name, user, password, host, port)  # return as a tuple


if __name__ == "__main__":
    main()
