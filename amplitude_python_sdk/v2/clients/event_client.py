"""Client implementation for the Amplitude V2 event API."""

from typing import List, Optional

import requests

from amplitude_python_sdk.v2 import routes
from amplitude_python_sdk.v2.exceptions.event import (
    InvalidRequestException,
    PayloadTooLargeException,
    TooManyRequestsForDeviceException,
)

from amplitude_python_sdk.v2.models.event import (
    Event,
    EventAPIOptions,
    UploadRequestBody,
    SuccessSummary,
)
from amplitude_python_sdk.common.utils import make_request


def wrap_exception(http_error: requests.HTTPError):
    resp = http_error.response
    exception_dict = {
        requests.codes.BAD_REQUEST: InvalidRequestException.from_response,
        requests.codes.REQUEST_ENTITY_TOO_LARGE: PayloadTooLargeException.from_response,
        requests.codes.TOO_MANY: TooManyRequestsForDeviceException.from_response,
    }
    exc_constructor = exception_dict.get(resp.status_code)
    if exc_constructor:
        return exc_constructor.__call__(resp)

    return http_error


class EventAPIClient:
    """
    See <https://developers.amplitude.com/docs/http-api-v2> for documentation.

    This client supports uploading events both via the batch endpoint
    and the regular event endpoint.
    """

    def __init__(self, api_key: str, api_endpoint: str = "https://api2.amplitude.com"):
        self.api_key = api_key
        self.api_endpoint = api_endpoint
        self.session = requests.Session()

    def _execute_upload(
        self,
        route: str,
        events: List[Event],
        options: Optional[EventAPIOptions] = None,
        timeout: int = 5,
    ) -> SuccessSummary:
        req_data = UploadRequestBody(
            api_key=self.api_key, events=events, options=options
        )
        json_data = req_data.model_dump_json(exclude_unset=True, exclude_none=True)
        try:
            resp = make_request(
                self.session,
                "POST",
                url=self.api_endpoint + route,
                data=json_data,
                headers={"Content-Type": "application/json"},
                timeout=timeout,
            )
            return SuccessSummary.model_validate_json(resp.content)
        except requests.HTTPError as exc:
            raise wrap_exception(exc)

    def upload(
        self,
        events: List[Event],
        options: Optional[EventAPIOptions] = None,
        timeout: int = 5,
    ) -> SuccessSummary:
        """
        Uploads events to Amplitude using the HTTP V2 API. See
        <https://developers.amplitude.com/docs/batch-event-upload-api#feature-comparison-between-httpapi-2httpapi--batch>
        for a comparison between this API and the batch API below.
        """
        return self._execute_upload(routes.EVENT_API, events, options, timeout)

    def batch_upload(
        self,
        events: List[Event],
        options: Optional[EventAPIOptions] = None,
        timeout: int = 5,
    ) -> SuccessSummary:
        """
        Uploads events to Amplitude using the Batch Event Upload API. See
        <https://developers.amplitude.com/docs/batch-event-upload-api#feature-comparison-between-httpapi-2httpapi--batch>
        for a comparison between this API and the HTTP V2 API above.
        """
        return self._execute_upload(routes.BATCH_API, events, options, timeout)
