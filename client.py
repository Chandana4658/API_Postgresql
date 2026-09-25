import requests


class APIClient:

    def __init__(self, base_url):

        self.base_url = base_url.rstrip("/")


    def get_data(self, endpoint):

        url = f"{self.base_url}/{endpoint}"

        response = requests.get(
            url,
            timeout=30
        )

        response.raise_for_status()

        return response.json()