"""Client implementation for the Amplitude V2 API."""

from typing import List, Optional, Dict, Any

import requests

from . import routes
from .models.event import EventV2
from .models.options import V2EventAPIOptions
from ..common.exceptions import AmplitudeAPIException
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

    def _construct_event_request_data(
        self, events: List[EventV2], options: Optional[V2EventAPIOptions]
    ) -> Dict[str, Any]:
        """
        Convert the strongly typed events and options into a dictionary payload
        matching the Amplitude API spec.
        """

        req_data = {
            "api_key": self.api_key,
            "events": [event.dict(exclude_none=True) for event in events],
        }
        if options:
            req_data["options"] = options.dict()
        return req_data

    def _log_events_internal(
        self, route: str, req_data: Dict[str, Any], timeout: int = 5,
    ) -> requests.Response:
        """
        Wrapper method that implements the underlying logic for both the
        HTTP V2 API and the Batch Event Upload API.
        """

        try:
            resp = requests.post(
                url=self.api_endpoint + route, json=req_data, timeout=timeout
            )
            return return_or_raise(resp)
        except requests.exceptions.Timeout as exc:
            raise AmplitudeAPIException() from exc

    def upload_events(
        self,
        events: List[EventV2],
        options: Optional[V2EventAPIOptions] = None,
        timeout: int = 5,
    ) -> requests.Response:
        """
        Logs events to Amplitude using the HTTP V2 API.
        See <https://developers.amplitude.com/docs/batch-event-upload-api#feature-comparison-between-httpapi-2httpapi--batch>
        for a comparison between this API and the batch API below.
        """  # pylint: disable=line-too-long
        req_data = self._construct_event_request_data(events, options)
        return self._log_events_internal(routes.EVENT_API, req_data, timeout)

    def batch_upload_events(
        self,
        events: List[EventV2],
        options: Optional[V2EventAPIOptions] = None,
        timeout: int = 5,
    ) -> requests.Response:
        """
        Logs events to Amplitude using the Batch Event Upload API. See
        <https://developers.amplitude.com/docs/batch-event-upload-api#feature-comparison-between-httpapi-2httpapi--batch>
        for a comparison between this API and the HTTP V2 API above.
        """  # pylint: disable=line-too-long
        req_data = self._construct_event_request_data(events, options)
        return self._log_events_internal(routes.BATCH_API, req_data, timeout)
