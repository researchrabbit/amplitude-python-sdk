"""Client implementation for the Amplitude V2 API."""

from typing import List, Optional

import requests

from .models.event import EventV2
from .models.options import V2EventAPIOptions
from ..common.utils import return_or_raise


class AmplitudeV2APIClient:  # pylint: disable=too-few-public-methods
    """
    See <https://developers.amplitude.com/docs/http-api-v2> for documentation.
    """

    def __init__(
        self, api_key: str, api_endpoint: str = "https://api2.amplitude.com/2"
    ):
        self.api_key = api_key
        self.api_endpoint = api_endpoint

    def send_events(
        self, events: List[EventV2], options: Optional[V2EventAPIOptions] = None
    ):  # pylint: disable=missing-function-docstring
        req_data = {
            "api_key": self.api_key,
            "events": [event.dict(exclude_none=True) for event in events],
        }
        if options:
            req_data["options"] = options.dict()
        resp = requests.post(
            url=self.api_endpoint + "/httpapi", json=req_data, timeout=5
        )
        return return_or_raise(resp)
