"""
    modules here :
"""
from typing import Dict

import requests

class Client:
    """
    Client class for handling API requests.
    """
    def __init__(self):
        """
        Initialize the Client class.
        """
        self.api: str = "https://oauth.telegram.org/auth{}".format
        self._api: str = "https://fragment.com{}".format
        self.session: requests.Session = requests.Session()
        self.timeout = 10
        self.headers: Dict[str, str] = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        }
        self.params: Dict[str, str] = {
            "bot_id": "5444323279", "origin": self._api(''),
            "request_access": "write", "return_to": self._api(''),
        }

    def auth_post(self, path: str, cookies: dict, data: dict, headers: dict):
        """
        Send a POST request to the authentication.
        """
        return requests.post(self.api(path), cookies=cookies, params=self.params ,data=data, headers={**self.headers, **headers}, timeout=self.timeout)

    def auth_get(self, path: str, cookies: dict, headers: dict):
        """
        Send a GET request to the authentication .
        """
        return requests.get(self.api(path), cookies=cookies, params=self.params, headers={**self.headers, **headers},timeout=self.timeout)
    
    def fr_post(self, path: str, data: dict, cookies: dict, headers: dict):
        """
        Send a POST request to the fragment .
        """
        return requests.post(self._api(path), cookies=cookies, params=self.params ,data=data, headers={**self.headers, **headers}, timeout=self.timeout)

    def fr_get(self, path: str, cookies: dict, headers: dict):
        """
        Send a GET request to the fragment .
        """
        return requests.get(self._api(path), cookies=cookies, params=self.params, headers={**self.headers, **headers}, timeout=self.timeout)


# # Example usage
# cli = Client()
# print(cli.fr_get('', cookies={}, headers={}).content)
