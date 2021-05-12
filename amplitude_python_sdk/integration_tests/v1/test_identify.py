import os

from dotenv import load_dotenv
import pytest
from requests import codes as status_codes, HTTPError

from amplitude_python_sdk.v1 import AmplitudeV1APIClient, Identification, UserProperties


@pytest.fixture(scope="module", autouse=True)
def load_env():
    load_dotenv()


@pytest.fixture(scope="module")
def test_api_key(load_env):
    return os.environ["AMPLITUDE_TEST_API_KEY"]


@pytest.fixture(scope="module")
def client(test_api_key):
    return AmplitudeV1APIClient(api_key=test_api_key)


@pytest.fixture
def idents():
    def _make_idents(length):
        set_fields = {"field1": True}
        set_once_fields = {"name": "Alice"}
        append_fields = {"foo2": "bar2"}
        prepend_fields = {"foo": "bar"}
        add_fields = {"view_count": 10}
        unset_fields = {"bad_field": "-"}
        remove_fields = {"sports": ["soccer", "football"]}
        up = UserProperties(
            set_fields=set_fields,
            set_once_fields=set_once_fields,
            add_fields=add_fields,
            append_fields=append_fields,
            prepend_fields=prepend_fields,
            unset_fields=unset_fields,
            remove_fields=remove_fields,
        )

        return [
            Identification(
                user_id=f"integration_test_user_{i}",
                device_id=f"integration_test_device_{i}",
                platform="web",
                os_name="Fake OS",
                language="en",
                paying="False",
                start_version="0.0.1",
                user_properties=up,
            )
            for i in range(length)
        ]

    return _make_idents


def test_identify_request_success(client, idents):
    """Use a small payload that'll pass testing."""
    request_data = idents(3)
    resp = client.identify(request_data)
    assert resp.status_code == status_codes.OK


def test_identify_request_too_large(client, idents):
    """Generate a payload large enough that it'll trigger a 413 Entity Too Large response from Amplitude."""
    request_data = idents(5000)
    with pytest.raises(HTTPError) as excinfo:
        client.identify(request_data)
        assert excinfo.response.status_code == status_codes.REQUEST_ENTITY_TOO_LARGE
