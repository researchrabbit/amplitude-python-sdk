"""Chart Annotations Client Tests"""
from datetime import date

import pytest
import requests
from requests import codes as status_codes

from amplitude_python_sdk.v2 import routes
from amplitude_python_sdk.v2.models.charts import (
    CreateChartAnnotationRequest,
    GetChartAnnotationResponse,
    ChartAnnotation,
    CreateChartAnnotationResponse,
    ListChartAnnotationsResponse,
)

from amplitude_python_sdk.v2.clients.chart_annotations_client import (
    ChartAnnotationsAPIClient,
)


@pytest.fixture
def chart_annotations_client():
    return ChartAnnotationsAPIClient(
        api_key="apikey",
        secret_key="secretkey",
        chart_annotations_api_endpoint="https://fake.researchrabbit",
    )


@pytest.fixture
def annotation_id():
    return 50079


@pytest.fixture
def annotation(annotation_id):
    return ChartAnnotation(date=date(2021, 5, 5), id=annotation_id, label="labels")


@pytest.fixture
def create_annotation_request():
    return CreateChartAnnotationRequest(
        app_id=50, date=date(2021, 5, 5), label="labels"
    )


@pytest.fixture
def create_annotation_response(annotation):
    return CreateChartAnnotationResponse(success=True, annotation=annotation)


@pytest.fixture
def get_annotation_response(annotation):
    return GetChartAnnotationResponse(annotation=annotation)


@pytest.fixture
def list_annotation_response():
    annotations = [
        ChartAnnotation(date=date(2021, 5, 4), id=i * 10, label=f"label_{i}")
        for i in range(100)
    ]
    return ListChartAnnotationsResponse(data=annotations)


def test_create_success(
    requests_mock,
    create_annotation_request: CreateChartAnnotationRequest,
    create_annotation_response: CreateChartAnnotationResponse,
    chart_annotations_client: ChartAnnotationsAPIClient,
):
    requests_mock.post(
        chart_annotations_client.chart_annotations_api_endpoint
        + routes.CHART_ANNOTATIONS_API,
        text=create_annotation_response.model_dump_json(),
    )

    response = chart_annotations_client.create(create_annotation_request)
    assert response == create_annotation_response


def test_create_fail(
    requests_mock,
    create_annotation_request: CreateChartAnnotationRequest,
    chart_annotations_client: ChartAnnotationsAPIClient,
):
    requests_mock.post(
        chart_annotations_client.chart_annotations_api_endpoint
        + routes.CHART_ANNOTATIONS_API,
        status_code=status_codes.BAD_REQUEST,
    )

    with pytest.raises(requests.HTTPError):
        chart_annotations_client.create(create_annotation_request)


def test_get_annotation_success(
    requests_mock,
    annotation_id: int,
    get_annotation_response: GetChartAnnotationResponse,
    chart_annotations_client: ChartAnnotationsAPIClient,
):
    requests_mock.get(
        chart_annotations_client.chart_annotations_api_endpoint
        + routes.CHART_ANNOTATIONS_API
        + f"/{annotation_id}",
        text=get_annotation_response.model_dump_json(),
    )

    resp = chart_annotations_client.get(annotation_id)
    assert resp == get_annotation_response


def test_get_annotation_fail(
    requests_mock,
    annotation_id: int,
    chart_annotations_client: ChartAnnotationsAPIClient,
):
    requests_mock.get(
        chart_annotations_client.chart_annotations_api_endpoint
        + routes.CHART_ANNOTATIONS_API
        + f"/{annotation_id}",
        status_code=status_codes.BAD_REQUEST,
    )

    with pytest.raises(requests.HTTPError):
        chart_annotations_client.get(annotation_id)


def test_list_annotations_success(
    requests_mock,
    list_annotation_response: ListChartAnnotationsResponse,
    chart_annotations_client: ChartAnnotationsAPIClient,
):
    requests_mock.get(
        chart_annotations_client.chart_annotations_api_endpoint
        + routes.CHART_ANNOTATIONS_API,
        text=list_annotation_response.model_dump_json(),
    )

    resp = chart_annotations_client.list()
    assert resp == list_annotation_response


def test_list_annotations_fail(
    requests_mock, chart_annotations_client: ChartAnnotationsAPIClient
):
    requests_mock.get(
        chart_annotations_client.chart_annotations_api_endpoint
        + routes.CHART_ANNOTATIONS_API,
        status_code=status_codes.BAD_REQUEST,
    )

    with pytest.raises(requests.HTTPError):
        chart_annotations_client.list()
