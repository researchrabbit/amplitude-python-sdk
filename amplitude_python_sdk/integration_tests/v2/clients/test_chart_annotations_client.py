from datetime import datetime
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


def test_create_and_get_chart_annotation(
    client: ChartAnnotationsAPIClient, test_project_id: str
):
    annotation = ChartAnnotation(
        app_id=test_project_id,
        date=datetime.now().date(),
        label="test_label",
        details="label used for integration testing",
    )
    resp = client.create(annotation)
    assert resp.status_code == status_codes.OK
    resp_data = resp.json()
    assert len(resp_data) == 2
    assert set(resp_data.keys()) == {"annotation", "success"}
    assert resp_data["success"] == True

    created_annotation = resp_data["annotation"]
    created_annotation_id = created_annotation.get("id")
    assert created_annotation_id is not None
    assert type(created_annotation_id) == int
    assert created_annotation.get("date") == str(annotation.date)
    assert created_annotation.get("details") == annotation.details
    assert created_annotation.get("label") == annotation.label

    resp = client.get(created_annotation_id)
    assert resp.status_code == status_codes.OK
    resp_data = resp.json()
    assert len(resp_data) == 1
    assert "annotation" in resp_data

    getd_annotation = resp_data.get("annotation")
    getd_annotation_id = getd_annotation.get("id")
    assert getd_annotation_id is not None
    assert type(getd_annotation_id) == int
    assert getd_annotation_id == created_annotation_id
    assert getd_annotation.get("date") == str(annotation.date)
    assert getd_annotation.get("details") == annotation.details
    assert getd_annotation.get("label") == annotation.label
