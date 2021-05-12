import pytest
import requests

from amplitude_python_sdk.v2.clients.event_client import EventAPIClient
from amplitude_python_sdk.v2.models.event import Event, EventAPIOptions


@pytest.fixture
def event_client():
    return EventAPIClient(api_key="fake")


@pytest.fixture
def events():
    return [
        Event(
            user_id=f"test_user_{i}",
            event_type="fake_event",
            event_properties={"prop1": "foo", "prop2": "bar"},
        )
        for i in range(10)
    ]


@pytest.fixture
def options():
    return EventAPIOptions(min_id_length=5)


def test_event_client(mocker, event_client, events, options):
    mock_response = requests.Response()
    mock_response.status_code = 200
    mock_response._content = {}  # pylint: disable=protected-access
    mocker.patch(
        "amplitude_python_sdk.v2.clients.event_client.make_request",
        return_value=mock_response,
    )

    event_client.upload(events, options)
    event_client.batch_upload(events, options)
