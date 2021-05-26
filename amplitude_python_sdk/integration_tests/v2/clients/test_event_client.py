from datetime import datetime
from typing import List

import pytest
from requests import codes as status_codes, HTTPError

from amplitude_python_sdk.v2.models.event import Event, EventAPIOptions
from amplitude_python_sdk.v2.clients import EventAPIClient


@pytest.fixture(scope="module")
def client(test_api_key: str):
    return EventAPIClient(api_key=test_api_key)


@pytest.fixture(scope="module")
def events():
    return [
        Event(
            user_id="integration_test_user",
            time=datetime.now(),
            event_type="integration_test_event",
            event_properties={"test_prop_1": "value_1", "test_prop_2": "value2"},
        )
        for _ in range(1, 5)
    ]


@pytest.fixture(scope="module")
def options():
    return EventAPIOptions(min_id_length=30)


def upload_empty_bad_request(client: EventAPIClient):
    with pytest.raises(HTTPError):
        client.upload([])


def batch_upload_empty_bad_request(client: EventAPIClient):
    with pytest.raises(HTTPError):
        client.batch_upload([])


def test_upload_events_successful(client: EventAPIClient, events: List[Event]):
    resp = client.upload(events)
    assert resp.code == status_codes.OK
    assert resp.events_ingested == len(events)


def test_batch_upload_events_successful(client: EventAPIClient, events: List[Event]):
    resp = client.batch_upload(events)
    assert resp.code == status_codes.OK
    assert resp.events_ingested == len(events)
