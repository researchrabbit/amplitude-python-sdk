from datetime import datetime
import os

import pytest

from amplitude_python_sdk.v2 import (
    ChartAnnotationsAPIClient,
    CreateChartAnnotationRequest,
)


@pytest.fixture(scope="module")
def test_project_id(load_env):
    """Amplitude test project ID that the annotations will be written to."""
    return os.environ["AMPLITUDE_TEST_PROJECT_ID"]


@pytest.fixture(scope="module")
def client(test_api_key: str, test_secret_key: str):
    return ChartAnnotationsAPIClient(api_key=test_api_key, secret_key=test_secret_key)


def test_list_chart_annotations(client: ChartAnnotationsAPIClient):
    resp = client.list()
    assert resp.data is not None
    assert len(resp.data) > 0


def test_create_and_get_chart_annotation(
    client: ChartAnnotationsAPIClient, test_project_id: str
):
    create_annotation_request = CreateChartAnnotationRequest(
        app_id=test_project_id,
        date=datetime.now().date(),
        label="test_label",
        details="label used for integration testing",
    )
    create_annotation_response = client.create(create_annotation_request)
    assert create_annotation_response.success is True
    assert create_annotation_response.annotation is not None
    assert create_annotation_response.annotation.id is not None
    assert create_annotation_response.annotation.date == create_annotation_request.date
    assert (
        create_annotation_response.annotation.details
        == create_annotation_request.details
    )
    assert (
        create_annotation_response.annotation.label == create_annotation_request.label
    )

    get_annotation_response = client.get(create_annotation_response.annotation.id)
    assert get_annotation_response.annotation is not None

    getd_annotation = get_annotation_response.annotation
    getd_annotation_id = getd_annotation.id
    assert getd_annotation_id is not None
    assert isinstance(getd_annotation_id, int)
    assert getd_annotation_id == create_annotation_response.annotation.id
    assert getd_annotation.date == create_annotation_request.date
    assert getd_annotation.details == create_annotation_request.details
    assert getd_annotation.label == create_annotation_request.label
