from datetime import datetime
import os

from dotenv import load_dotenv
import pytest
from requests import codes as status_codes

from amplitude_python_sdk.v2.models import Event, EventAPIOptions
from amplitude_python_sdk.v2.clients import EventAPIClient


@pytest.fixture(scope="module", autouse=True)
def load_env():
    load_dotenv()


@pytest.fixture(scope="module")
def test_api_key(load_env):
    return os.environ["AMPLITUDE_TEST_API_KEY"]


@pytest.fixture(scope="module")
def client(test_api_key: str):
    return EventAPIClient(api_key=test_api_key)


@pytest.fixture(scope="module")
def events():
    return [
        Event(user_id="integration_test_user", event_type="integration_test_event")
        for i in range(1, 5)
    ]


@pytest.fixture(scope="module")
def options():
    return EventAPIOptions(min_id_length=30)


def upload_empty_bad_request(client: EventAPIClient):
    resp = client.upload([])
    assert resp.status_code == status_codes.BAD_REQUEST
    batch_resp = client.batch_upload([])
    assert batch_resp.status_code == status_codes.BAD_REQUEST


def test_upload_events_successful(client: EventAPIClient, events: List[Event]):
    resp = client.upload(events)
    assert resp.status_code == status_codes.OK
