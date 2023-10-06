import datetime
import re
import time

import psycopg2


def main():
    requests_that_took_1_second = []
    query = """
        SELECT
            "custom_user_user"."id",
            "custom_user_user"."password",
            "custom_user_user"."last_login",
            "custom_user_user"."uuid",
            "custom_user_user"."username",
            "custom_user_user"."first_name",
            "custom_user_user"."last_name",
            "custom_user_user"."email",
            "custom_user_user"."email_verified",
            "custom_user_user"."email_verified_date",
            "custom_user_user"."email_verified_sources",
            "custom_user_user"."is_superuser",
            "custom_user_user"."phone",
            "custom_user_user"."phone_verified_on",
            "custom_user_user"."is_staff",
            "custom_user_user"."is_active",
            "custom_user_user"."ou_id",
            "custom_user_user"."date_joined",
            "custom_user_user"."modified",
            "custom_user_user"."last_account_deletion_alert",
            "custom_user_user"."deactivation",
            "custom_user_user"."deactivation_reason",
            "custom_user_user"."keepalive"
        FROM
            "custom_user_user"
        ORDER BY
            "custom_user_user"."last_name" ASC,
            "custom_user_user"."first_name" ASC,
            "custom_user_user"."email" ASC,
            "custom_user_user"."username" ASC
        LIMIT 1
    """
    database, user, password, host, port, schema = get_psql_cmd_details()
    for i in range(1, 1001):
        start_time = time.time()
        connection = psycopg2.connect(
            host=host,
            port=port,
            database=database,
            user=user,
            password=password,
        )
        cursor = connection.cursor()
        cursor.execute(f"set schema '{schema}';")
        cursor.execute(query)
        cursor.close()
        end_time = time.time()
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        duration = end_time - start_time
        result_str = f"[{timestamp}] {i} {duration}"
        if duration > 1:
            requests_that_took_1_second.append(result_str)
        print(result_str)

    if requests_that_took_1_second:
        print("\n\n\nRequests that took more than 1 second:\n")
        for request in requests_that_took_1_second:
            print(request, end="\n")
    else:
        print("\n\n\nNo request took more than 1 second.", "I guess it's ok.")


def get_psql_cmd_details():
    with open("/etc/authentic2-multitenant/settings.d/config.py", "r") as file:
        content = file.read()

        database_name = re.search(
            r"DATABASES\['default'\]\['NAME'\] = '(.+?)'", content
        ).group(1)
        user = re.search(r"DATABASES\['default'\]\['USER'\] = '(.+?)'", content).group(
            1
        )
        password = re.search(
            r"DATABASES\['default'\]\['PASSWORD'\] = '(.+?)'", content
        ).group(1)
        host = re.search(r"DATABASES\['default'\]\['HOST'\] = '(.+?)'", content).group(
            1
        )
        port = re.search(r"DATABASES\['default'\]\['PORT'\] = '(.+?)'", content).group(
            1
        )
        hostname_match = re.search(r"ALLOWED_HOSTS = \[\s*'(.+?)'", content)
        schema = None
        if hostname_match:
            domain = hostname_match.group(1)
            schema = domain.replace("-", "_").replace(".", "_")
            print(
                f"Found schema {schema} (extracted and parsed from ALLOWED_HOSTS in "
                "config.py, may be wrong)"
            )
        else:
            print(
                "Could not find ALLOWED_HOSTS in "
                "/etc/authentic2-multitenant/settings.d/config.py\nYou gave to manually "
                "specify the 'set schema' in the query, editing this script.\nExample:\nset "
                "schema 'mettet_auth_guichet_citoyen_be';"
            )

    return (database_name, user, password, host, port, schema)  # return as a tuple


if __name__ == "__main__":
    main()
