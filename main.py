from client import APIClient
from connection import get_connection
import json
from pathlib import Path


def extract_data():
    print("\n[1] Extracting data from API...")

    client = APIClient(
        "https://jsonplaceholder.typicode.com"
    )

    users = client.get_data("users")

    Path("raw").mkdir(
        parents=True,
        exist_ok=True
    )

    with open(
        "raw/users.json",
        "w",
        encoding="utf-8"
    ) as file:
        json.dump(
            users,
            file,
            indent=4
        )

    print(
        f"Extracted {len(users)} customer records."
    )


def load_customers():
    print("\n[2] Loading customers into PostgreSQL...")

    with open(
        "raw/users.json",
        "r",
        encoding="utf-8"
    ) as file:
        users = json.load(file)

    connection = get_connection()
    cursor = connection.cursor()

    for user in users:

        cursor.execute(
            """
            INSERT INTO customers
            (
                customer_id,
                name,
                email,
                city
            )
            VALUES (%s, %s, %s, %s)

            ON CONFLICT (customer_id)
            DO UPDATE SET
                name = EXCLUDED.name,
                email = EXCLUDED.email,
                city = EXCLUDED.city;
            """,
            (
                user["id"],
                user["name"],
                user["email"],
                user["address"]["city"]
            )
        )

    connection.commit()

    cursor.close()
    connection.close()

    print(
        f"Loaded {len(users)} customers into PostgreSQL."
    )


def validate_connection():

    print("\n[3] Validating PostgreSQL data...")

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM customers;"
    )

    total = cursor.fetchone()[0]

    print(
        f"Total customers in database: {total}"
    )

    cursor.close()
    connection.close()


def main():

    print("=" * 55)
    print(" API → POSTGRESQL DATA INGESTION PIPELINE")
    print("=" * 55)

    try:

        extract_data()

        load_customers()

        validate_connection()

        print("\nPipeline completed successfully!")

    except Exception as error:

        print(
            f"\nPipeline failed: {error}"
        )


if __name__ == "__main__":
    main()
    