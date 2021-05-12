"""Client implementation for the Amplitude V2 event API."""

from typing import List, Optional

import requests

from amplitude_python_sdk.v2 import routes

from amplitude_python_sdk.v2.models.event import (
    Event,
    EventAPIOptions,
    UploadRequestBody,
)
from amplitude_python_sdk.common.utils import make_request


class EventAPIClient:
    """
    See <https://developers.amplitude.com/docs/http-api-v2> for documentation.

    This client supports uploading events both via the batch endpoint
    and the regular event endpoint.
    """

    def __init__(
        self, api_key: str, api_endpoint: str = "https://api2.amplitude.com/2"
    ):
        self.api_key = api_key
        self.api_endpoint = api_endpoint
        self.session = requests.Session()

    def upload(
        self,
        events: List[Event],
        options: Optional[EventAPIOptions] = None,
        timeout: int = 5,
    ) -> requests.Response:
        """
        Uploads events to Amplitude using the HTTP V2 API.
        See <https://developers.amplitude.com/docs/batch-event-upload-api#feature-comparison-between-httpapi-2httpapi--batch>
        for a comparison between this API and the batch API below.
        """  # pylint: disable=line-too-long
        req_data = UploadRequestBody(
            api_key=self.api_key, events=events, options=options
        )
        json_data = req_data.dict(exclude_unset=True, exclude_none=True)
        return make_request(
            self.session,
            "POST",
            url=self.api_endpoint + routes.EVENT_API,
            json=json_data,
            timeout=timeout,
        )

    def batch_upload(
        self,
        events: List[Event],
        options: Optional[EventAPIOptions] = None,
        timeout: int = 5,
    ) -> requests.Response:
        """
        Uploads events to Amplitude using the Batch Event Upload API. See
        <https://developers.amplitude.com/docs/batch-event-upload-api#feature-comparison-between-httpapi-2httpapi--batch>
        for a comparison between this API and the HTTP V2 API above.
        """  # pylint: disable=line-too-long
        req_data = UploadRequestBody(
            api_key=self.api_key, events=events, options=options
        )
        json_data = req_data.dict(exclude_unset=True, exclude_none=True)
        return make_request(
            self.session,
            "POST",
            url=self.api_endpoint + routes.BATCH_API,
            json=json_data,
            timeout=timeout,
        )
