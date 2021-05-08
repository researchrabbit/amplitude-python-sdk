"""Chart Annotations Client Tests"""

import requests
from unittest.mock import patch

from datetime import date
from amplitude_python_sdk.v2.models.charts import ChartAnnotations

from amplitude_python_sdk.v2.clients.chart_annotations_client import ChartAnnotationsAPIClient

_chart_annotations_client_ = ChartAnnotationsAPIClient(api_key='apikey', secret_key='secretkey')
_annotation_ = ChartAnnotations(app_id=50, date=date(2021, 5, 5), label='labels')
_annotation_id = '50079'
_annotation_get_response = {
    "annotation": {
        "date": "2021-05-05",
        "details": "",
        "id": 50079,
        "label": "labels"
    }
}

_annotation_create_response = {
    "annotation": {
        "date": "2021-05-05",
        "details": "",
        "id": 50079,
        "label": "labels"
    },
    "success": True
}


@patch('amplitude_python_sdk.common.utils.make_request')
def test_create_success(mock_request):
    mock_response = requests.Response()
    mock_response.status_code = 200
    mock_response._content = _annotation_create_response
    mock_request.return_value = mock_response

    resp = _chart_annotations_client_.create(_annotation_)
    assert resp._content == _annotation_create_response


@patch('amplitude_python_sdk.common.utils.make_request')
def test_create_fail(mock_request):
    mock_response = requests.Response()
    mock_response.status_code = 400
    mock_request.return_value = mock_response

    resp = _chart_annotations_client_.create(_annotation_)
    assert resp.status_code == 400


@patch('amplitude_python_sdk.common.utils.make_request')
def test_get_annotation_id_success(mock_request):
    mock_response = requests.Response()
    mock_response.status_code = 200
    mock_response._content = _annotation_get_response
    mock_request.return_value = mock_response

    resp = _chart_annotations_client_.get(_annotation_id)
    assert resp._content == _annotation_get_response


@patch('amplitude_python_sdk.common.utils.make_request')
def test_gt_annotation_id_fail(mock_request):
    mock_response = requests.Response()
    mock_response.status_code = 400
    mock_request.return_value = mock_response

    resp = _chart_annotations_client_.get(_annotation_id)
    assert resp.status_code == 400


@patch('amplitude_python_sdk.common.utils.make_request')
def test_get_success(mock_request):
    mock_response = requests.Response()
    mock_response.status_code = 200
    mock_response._content = _annotation_get_response
    mock_request.return_value = mock_response

    resp = _chart_annotations_client_.get()
    assert resp._content == _annotation_get_response


@patch('amplitude_python_sdk.common.utils.make_request')
def test_get_fail(mock_request):
    mock_response = requests.Response()
    mock_response.status_code = 400
    mock_request.return_value = mock_response

    resp = _chart_annotations_client_.get()
    assert resp.status_code == 400
