import json
from typing import List

import requests

from . import routes
from .models.identify import Identification


class AmplitudeClient:

    def __init__(self, api_key, api_endpoint='https://api.amplitude.com'):
        self.api_key = api_key
        self.api_endpoint = api_endpoint

    def identify(self, request: List[Identification]):
        identify_url = self.api_endpoint + routes.IDENTIFY
        req_data = {
            'api_key': self.api_key,
            'identification': json.dumps([req.payload for req in request]),
        }
        resp = requests.post(data=req_data, url=identify_url, timeout=1)
        resp.raise_for_status()
        return resp


