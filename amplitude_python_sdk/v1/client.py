"""
Client implementation which can be used to call the various Amplitude API methods.
"""

from typing import List

import requests

from . import routes
from .models.identify import Identification, IdentifyAPIRequest
from ..common.utils import make_request


class AmplitudeV1APIClient:
    def __init__(self, api_key, api_endpoint="https://api.amplitude.com"):
        self.api_key = api_key
        self.api_endpoint = api_endpoint
        self.session = requests.Session()

    def identify(
        self, ids: List[Identification], timeout: int = 5
    ) -> requests.Response:
        """
        See <https://developers.amplitude.com/docs/identify-api> for official docs.

        :param ids A list of Identification objects representing the users to identify
                   and their properties.
        :param timeout Number of seconds before the Amplitude request is marked as timed out.
        :return: The response from the Amplitude API.
        """
        identify_url = self.api_endpoint + routes.IDENTIFY
        req_data = IdentifyAPIRequest.from_ids(self.api_key, ids)

        # Note - this API deliberately posts the JSON string as form data, in line with
        # the Amplitude documentation (see link above).
        return make_request(
            self.session,
            "POST",
            identify_url,
            data=req_data.model_dump(),
            timeout=timeout,
        )
