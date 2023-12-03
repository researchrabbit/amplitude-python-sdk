import time
from typing import List

import pytest
from requests import codes as status_codes, HTTPError

from amplitude_python_sdk.v2 import routes
from amplitude_python_sdk.v2.clients.event_client import EventAPIClient
from amplitude_python_sdk.v2.exceptions.event import (
    InvalidRequestException,
    PayloadTooLargeException,
    TooManyRequestsForDeviceException,
)
from amplitude_python_sdk.v2.models.event import (
    Event,
    EventAPIOptions,
    SuccessSummary,
    InvalidRequestError,
    PayloadTooLargeError,
    TooManyRequestsForDeviceError,
)


@pytest.fixture
def event_client() -> EventAPIClient:
    return EventAPIClient(api_key="fake")


@pytest.fixture
def events() -> List[Event]:
    return [
        Event(
            user_id=f"test_user_{i}",
            event_type="fake_event",
            event_properties={"prop1": "foo", "prop2": "bar"},
        )
        for i in range(10)
    ]


@pytest.fixture
def options() -> EventAPIOptions:
    return EventAPIOptions(min_id_length=5)


@pytest.fixture
def upload_success_response(events: List[Event]) -> SuccessSummary:
    return SuccessSummary(
        code=status_codes.OK,
        events_ingested=len(events),
        payload_size_bytes=200,
        server_upload_time=int(time.time()),
    )


@pytest.fixture
def invalid_request_error() -> InvalidRequestError:
    return InvalidRequestError(
        code=status_codes.BAD_REQUEST, error="invalid payload", missing_field="time"
    )


@pytest.fixture
def payload_too_large_error() -> PayloadTooLargeError:
    return PayloadTooLargeError(
        code=status_codes.REQUEST_ENTITY_TOO_LARGE, error="too many events"
    )


@pytest.fixture
def too_many_requests_for_device_error() -> TooManyRequestsForDeviceError:
    return TooManyRequestsForDeviceError(
        code=status_codes.TOO_MANY,
        error="Too many requests for device",
        eps_threshold=5,
    )


def test_upload(
    requests_mock,
    event_client: EventAPIClient,
    events: List[Event],
    options: EventAPIOptions,
    upload_success_response: SuccessSummary,
):
    requests_mock.post(
        event_client.api_endpoint + routes.EVENT_API,
        text=upload_success_response.model_dump_json(),
    )
    resp = event_client.upload(events, options)
    assert resp == upload_success_response


def test_batch_upload(
    requests_mock,
    event_client: EventAPIClient,
    events: List[Event],
    options: EventAPIOptions,
    upload_success_response: SuccessSummary,
):
    requests_mock.post(
        event_client.api_endpoint + routes.BATCH_API,
        text=upload_success_response.model_dump_json(),
    )
    resp = event_client.batch_upload(events, options)
    assert resp == upload_success_response


def test_invalid_request(
    requests_mock,
    event_client: EventAPIClient,
    events: List[Event],
    options: EventAPIOptions,
    invalid_request_error: InvalidRequestError,
):
    requests_mock.post(
        event_client.api_endpoint + routes.BATCH_API,
        text=invalid_request_error.model_dump_json(),
        status_code=status_codes.BAD_REQUEST,
    )
    requests_mock.post(
        event_client.api_endpoint + routes.EVENT_API,
        text=invalid_request_error.model_dump_json(),
        status_code=status_codes.BAD_REQUEST,
    )
    with pytest.raises(InvalidRequestException) as exc:
        event_client.batch_upload(events, options)
        assert exc.error == invalid_request_error
    with pytest.raises(InvalidRequestException) as exc:
        event_client.upload(events, options)
        assert exc.error == invalid_request_error


def test_payload_too_large(
    requests_mock,
    event_client: EventAPIClient,
    events: List[Event],
    options: EventAPIOptions,
    payload_too_large_error: PayloadTooLargeError,
):
    requests_mock.post(
        event_client.api_endpoint + routes.BATCH_API,
        text=payload_too_large_error.model_dump_json(),
        status_code=status_codes.REQUEST_ENTITY_TOO_LARGE,
    )
    requests_mock.post(
        event_client.api_endpoint + routes.EVENT_API,
        text=payload_too_large_error.model_dump_json(),
        status_code=status_codes.REQUEST_ENTITY_TOO_LARGE,
    )
    with pytest.raises(PayloadTooLargeException) as exc:
        event_client.batch_upload(events, options)
        assert exc.error == payload_too_large_error
    with pytest.raises(PayloadTooLargeException) as exc:
        event_client.upload(events, options)
        assert exc.error == payload_too_large_error


def test_too_many_requests(
    requests_mock,
    event_client: EventAPIClient,
    events: List[Event],
    options: EventAPIOptions,
    too_many_requests_for_device_error: TooManyRequestsForDeviceError,
):
    requests_mock.post(
        event_client.api_endpoint + routes.BATCH_API,
        text=too_many_requests_for_device_error.model_dump_json(),
        status_code=status_codes.TOO_MANY,
    )
    requests_mock.post(
        event_client.api_endpoint + routes.EVENT_API,
        text=too_many_requests_for_device_error.model_dump_json(),
        status_code=status_codes.TOO_MANY,
    )
    with pytest.raises(TooManyRequestsForDeviceException) as exc:
        event_client.batch_upload(events, options)
        assert exc.error == too_many_requests_for_device_error
    with pytest.raises(TooManyRequestsForDeviceException) as exc:
        event_client.upload(events, options)
        assert exc.error == too_many_requests_for_device_error


def test_other_error(
    requests_mock,
    event_client: EventAPIClient,
    events: List[Event],
    options: EventAPIOptions,
):
    requests_mock.post(
        event_client.api_endpoint + routes.BATCH_API,
        status_code=status_codes.SERVER_ERROR,
    )
    requests_mock.post(
        event_client.api_endpoint + routes.EVENT_API,
        status_code=status_codes.SERVER_ERROR,
    )
    with pytest.raises(HTTPError):
        event_client.batch_upload(events, options)
    with pytest.raises(HTTPError):
        event_client.upload(events, options)
