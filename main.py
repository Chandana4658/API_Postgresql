from api.api_client import APIClient


def main():

    client = APIClient(
        "https://jsonplaceholder.typicode.com"
    )

    users = client.get_data("users")

    print("Records extracted:", len(users))

    print("\nFirst record:")
    print(users[0])


if __name__ == "__main__":
    main()