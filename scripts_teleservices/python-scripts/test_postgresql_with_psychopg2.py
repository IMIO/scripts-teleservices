import datetime
import time

import psycopg2


def main():
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

    for i in range(1, 1001):
        start_time = time.time()
        connection = psycopg2.connect(
            host="10.7.131.3",
            port="5432",
            database="teleservices_mettet_authentic2",
            user="teleservices_mettet",
            password="dTAaBesFc76LccIZ",
        )
        cursor = connection.cursor()
        cursor.execute("set schema 'mettet_auth_guichet_citoyen_be';")
        cursor.execute(query)
        cursor.close()
        end_time = time.time()
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] {i} {end_time - start_time}")


if __name__ == "__main__":
    main()
