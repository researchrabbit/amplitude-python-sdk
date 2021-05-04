"""Test file for the functions in the utils package."""

import pytest
import requests
import httpretty

from amplitude_python_sdk.common.utils import make_request, return_or_raise
from amplitude_python_sdk.common.exceptions import AmplitudeAPIException


def test_return_or_raise_failed_status():
    """Test a response with a failure status, and ensure that it correctly fails."""
    response = requests.Response()
    response.status_code = 400
    response._content = (  # pylint: disable=protected-access
        b'{"error": "Failed to call Amplitude"}'
    )
    with pytest.raises(AmplitudeAPIException):
        return_or_raise(response)


def test_return_or_raise_success():
    """Test a response with a success status, and ensure that it does not fail."""
    response = requests.Response()
    response.status_code = 200
    response._content = (  # pylint: disable=protected-access
        b'{"error": "Failed to call Amplitude"}'
    )
    assert return_or_raise(response) == response


@httpretty.activate
def test_make_request_timeout():
    def timeoutCallback(request, uri, headers):
        raise requests.Timeout("Connection timed out.")

    httpretty.register_uri(
        httpretty.GET,
        "http://fake.researchrabbit",
        status=200,
        body=timeoutCallback,
    )

    session = requests.Session()
    with pytest.raises(AmplitudeAPIException) as excinfo:
        make_request(session, "GET", "http://fake.researchrabbit")
        assert isinstance(excinfo.__cause__, requests.Timeout)


@httpretty.activate
def test_make_request_failure():
    httpretty.register_uri(
        httpretty.GET,
        "http://fake.researchrabbit",
        status=400,
        body="failure",
    )

    session = requests.Session()
    with pytest.raises(AmplitudeAPIException) as excinfo:
        resp = make_request(session, "GET", "http://fake.researchrabbit")
        assert isinstance(excinfo.__cause__, requests.HTTPError)


@httpretty.activate
def test_make_request_success():
    httpretty.register_uri(
        httpretty.GET,
        "http://fake.researchrabbit",
        status=200,
        body="success",
    )

    session = requests.Session()
    resp = make_request(session, "GET", "http://fake.researchrabbit")
    assert resp.text == "success"
