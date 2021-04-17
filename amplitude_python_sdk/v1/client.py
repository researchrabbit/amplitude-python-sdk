"""
Client implementation which can be used to call the various Amplitude API methods.
"""

import json
from typing import List

import requests

from . import routes
from .models.identify import Identification
from ..common.utils import return_or_raise


class AmplitudeV1APIClient:  # pylint: disable=missing-class-docstring,too-few-public-methods
    def __init__(self, api_key, api_endpoint="https://api.amplitude.com"):
        self.api_key = api_key
        self.api_endpoint = api_endpoint

    def identify(self, ids: List[Identification]) -> requests.Response:
        """
        See <https://developers.amplitude.com/docs/identify-api> for official docs.

        :param ids A list of Identification objects representing the users to identify
                   and their properties.
        :return: The response from the Amplitude API.
        """
        identify_url = self.api_endpoint + routes.IDENTIFY
        req_data = {
            "api_key": self.api_key,
            "identification": json.dumps([req.payload for req in ids]),
        }
        resp = requests.post(data=req_data, url=identify_url, timeout=5)
        return return_or_raise(resp)
