import os

from dotenv import load_dotenv
import pytest
from requests import codes as status_codes

from amplitude_python_sdk.v2 import ChartAnnotationsAPIClient, ChartAnnotation


@pytest.fixture(scope="module", autouse=True)
def load_env():
    load_dotenv()


@pytest.fixture(scope="module")
def test_api_key(load_env):
    return os.environ["AMPLITUDE_TEST_API_KEY"]


@pytest.fixture(scope="module")
def test_secret_key(load_env):
    return os.environ["AMPLITUDE_TEST_SECRET_KEY"]


@pytest.fixture(scope="module")
def test_project_id(load_env):
    """Amplitude test project ID that the annotations will be written to."""
    return os.environ["AMPLITUDE_TEST_PROJECT_ID"]


@pytest.fixture(scope="module")
def client(test_api_key: str, test_secret_key: str):
    return ChartAnnotationsAPIClient(api_key=test_api_key, secret_key=test_secret_key)


def test_list_chart_annotations(client: ChartAnnotationsAPIClient):
    resp = client.list()
    assert resp.status_code == status_codes.OK


def test_create_chart_annotation(
    client: ChartAnnotationsAPIClient, test_project_id: str
):
    annotation = ChartAnnotation()
    resp = client.create()


def test_retrieve_chart_annotation():
    pass
