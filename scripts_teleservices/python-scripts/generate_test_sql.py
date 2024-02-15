"""
Generates a sql file with many repetitions of a query and prints the psql command to
execute the file.

--print-psql-cmd will print the psql command to run the script.


Usage:

python3 generate_test_sql_file.py
"""

import argparse
import re


def main():
    """Generate a sql file with many repetitions of a query."""
    if args.print_psql_cmd:
        print(get_psql_cmd_details())
        return
    repetitions = 1000
    filename = "test.sql"
    schema = get_psql_schema()
    generate_sql_file(filename, repetitions, schema=schema)
    print(f"Generated {filename} with {repetitions} repetitions.")
    psql_command_details = get_psql_cmd_details()
    print("Generated psql cmd:", psql_command_details, " -f test.sql")


def get_psql_schema():
    """Get the schema from the settings file."""
    with open("/etc/authentic2-multitenant/settings.d/config.py", "r") as file:
        content = file.read()

    hostname_match = re.search(r"ALLOWED_HOSTS = \[\s*'(.+?)'", content)
    if hostname_match:
        domain = hostname_match.group(1)
        schema = domain.replace("-", "_").replace(".", "_")
        print(f"Found schema {schema} (extracted and parsed from ALLOWED_HOSTS in " "config.py, may be wrong)")
    else:
        print(
            "Could not find ALLOWED_HOSTS in "
            "/etc/authentic2-multitenant/settings.d/config.py\nYou gave to manually "
            "specify the schema at the top of the generated sql file.\nExample:\nset "
            "schema 'mettet_auth_guichet_citoyen_be';"
        )

    return schema


def get_psql_cmd_details():
    with open("/etc/authentic2-multitenant/settings.d/config.py", "r") as file:
        content = file.read()

    database_name = re.search(r"DATABASES\['default'\]\['NAME'\] = '(.+?)'", content).group(1)
    user = re.search(r"DATABASES\['default'\]\['USER'\] = '(.+?)'", content).group(1)
    password = re.search(r"DATABASES\['default'\]\['PASSWORD'\] = '(.+?)'", content).group(1)
    host = re.search(r"DATABASES\['default'\]\['HOST'\] = '(.+?)'", content).group(1)
    port = re.search(r"DATABASES\['default'\]\['PORT'\] = '(.+?)'", content).group(1)

    psql_cmd = f"PGPASSWORD={password} psql -U {user} -h {host} -p {port} -d {database_name}"

    return psql_cmd


def generate_sql_file(filename="test.sql", repetitions=1000, schema=None):
    query = (
        'SELECT "custom_user_user"."id", "custom_user_user"."password", '
        '"custom_user_user"."last_login", "custom_user_user"."uuid", '
        '"custom_user_user"."username", "custom_user_user"."first_name", '
        '"custom_user_user"."last_name", "custom_user_user"."email", '
        '"custom_user_user"."email_verified", "custom_user_user"."email_verified_date", '
        '"custom_user_user"."email_verified_sources", "custom_user_user"."is_superuser", '
        '"custom_user_user"."phone", "custom_user_user"."phone_verified_on", '
        '"custom_user_user"."is_staff", "custom_user_user"."is_active", '
        '"custom_user_user"."ou_id", "custom_user_user"."date_joined", '
        '"custom_user_user"."modified", "custom_user_user"."last_account_deletion_alert", '
        '"custom_user_user"."deactivation", "custom_user_user"."deactivation_reason", '
        '"custom_user_user"."keepalive" FROM "custom_user_user" ORDER BY '
        '"custom_user_user"."last_name" ASC, "custom_user_user"."first_name" ASC, '
        '"custom_user_user"."email" ASC, "custom_user_user"."username" ASC;\n'
    )
    with open(filename, "w") as file:
        if schema:
            file.write(f"set schema '{schema}';\n")
        file.write(query * repetitions)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a sql file with many repetitions of a query.")
    parser.add_argument(
        "--print-psql-cmd",
        action="store_true",
        help="Print the psql command to run the script.",
    )
    args = parser.parse_args()
    main()
