"""Chart Annotations Client Tests"""
from datetime import date

import pytest
import requests

from amplitude_python_sdk.v2.models.charts import ChartAnnotations

from amplitude_python_sdk.v2.clients.chart_annotations_client import (
    ChartAnnotationsAPIClient,
)


@pytest.fixture
def chart_annotations_client():
    return ChartAnnotationsAPIClient(api_key="apikey", secret_key="secretkey")


@pytest.fixture
def annotation():
    return ChartAnnotations(app_id=50, date=date(2021, 5, 5), label="labels")


@pytest.fixture
def annotation_id():
    return "50079"


@pytest.fixture
def annotation_get_response():
    return {
        "annotation": {
            "date": "2021-05-05",
            "details": "",
            "id": 50079,
            "label": "labels",
        }
    }


@pytest.fixture
def annotation_create_response():
    return {
        "annotation": {
            "date": "2021-05-05",
            "details": "",
            "id": 50079,
            "label": "labels",
        },
        "success": True,
    }


def test_create_success(
    mocker, annotation, annotation_create_response, chart_annotations_client  # pylint: disable=redefined-outer-name
):
    mock_response = requests.Response()
    mock_response.status_code = 200
    mock_response._content = (  # pylint: disable=protected-access
        annotation_create_response
    )
    mocker.patch(
        "amplitude_python_sdk.v2.clients.chart_annotations_client.make_request",
        return_value=mock_response,
    )

    resp = chart_annotations_client.create(annotation)
    assert resp.content == annotation_create_response


def test_create_fail(mocker, annotation, chart_annotations_client):  # pylint: disable=redefined-outer-name
    mock_response = requests.Response()
    mock_response.status_code = 400
    mocker.patch(
        "amplitude_python_sdk.v2.clients.chart_annotations_client.make_request",
        return_value=mock_response,
    )

    resp = chart_annotations_client.create(annotation)
    assert resp.status_code == 400


def test_get_annotation_id_success(
    mocker, annotation_id, annotation_get_response, chart_annotations_client  # pylint: disable=redefined-outer-name
):
    mock_response = requests.Response()
    mock_response.status_code = 200
    mock_response._content = annotation_get_response  # pylint: disable=protected-access
    mocker.patch(
        "amplitude_python_sdk.v2.clients.chart_annotations_client.make_request",
        return_value=mock_response,
    )

    resp = chart_annotations_client.get(annotation_id)
    assert resp.content == annotation_get_response


def test_gt_annotation_id_fail(mocker, annotation_id, chart_annotations_client):  # pylint: disable=redefined-outer-name
    mock_response = requests.Response()
    mock_response.status_code = 400
    mocker.patch(
        "amplitude_python_sdk.v2.clients.chart_annotations_client.make_request",
        return_value=mock_response,
    )

    resp = chart_annotations_client.get(annotation_id)
    assert resp.status_code == 400


def test_get_success(mocker, annotation_get_response, chart_annotations_client):  # pylint: disable=redefined-outer-name
    mock_response = requests.Response()
    mock_response.status_code = 200
    mock_response._content = annotation_get_response  # pylint: disable=protected-access
    mocker.patch(
        "amplitude_python_sdk.v2.clients.chart_annotations_client.make_request",
        return_value=mock_response,
    )

    resp = chart_annotations_client.get()
    assert resp.content == annotation_get_response  # pylint: disable=protected-access


def test_get_fail(mocker, chart_annotations_client):  # pylint: disable=redefined-outer-name
    mock_response = requests.Response()
    mock_response.status_code = 400
    mocker.patch(
        "amplitude_python_sdk.v2.clients.chart_annotations_client.make_request",
        return_value=mock_response,
    )

    resp = chart_annotations_client.get()
    assert resp.status_code == 400
