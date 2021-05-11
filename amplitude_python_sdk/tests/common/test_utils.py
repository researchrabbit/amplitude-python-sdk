"""Test file for the functions in the utils package."""

import pytest
import requests
import httpretty

from amplitude_python_sdk.common.utils import make_request, return_or_raise


@pytest.fixture
def fake_url():
    return "https://fake.researchrabbit"


def test_return_or_raise_failed_status():
    """Test a response with a failure status, and ensure that it correctly fails."""
    response = requests.Response()
    response.status_code = 400
    response._content = (  # pylint: disable=protected-access
        b'{"error": "Failed to call Amplitude"}'
    )
    with pytest.raises(requests.HTTPError):
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
def test_make_request_timeout(fake_url):
    def timeoutCallback(request, uri, headers):
        raise requests.Timeout("Connection timed out.")

    httpretty.register_uri(
        httpretty.GET,
        fake_url,
        status=200,
        body=timeoutCallback,
    )

    session = requests.Session()
    with pytest.raises(requests.Timeout):
        make_request(session, "GET", fake_url)


@httpretty.activate
def test_make_request_failure(fake_url):
    httpretty.register_uri(
        httpretty.GET,
        fake_url,
        status=400,
        body="failure",
    )

    session = requests.Session()
    with pytest.raises(requests.HTTPError):
        make_request(session, "GET", fake_url)


@httpretty.activate
def test_make_request_success(fake_url):
    httpretty.register_uri(
        httpretty.GET,
        fake_url,
        status=200,
        body="success",
    )

    session = requests.Session()
    resp = make_request(session, "GET", fake_url)
    assert resp.text == "success"
