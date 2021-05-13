"""Base classes for clients used in other packages."""

from abc import ABC

import requests


class BaseClient(ABC):
    def __init__(self):
        self.session = requests.Session()


class BasicAuthAPIClient(BaseClient, ABC):
    def __init__(self, api_key: str, secret_key: str):
        super().__init__()
        self.session.auth = (api_key, secret_key)
