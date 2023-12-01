"""Test file for the functions in the utils package."""

import pytest
from requests import codes as status_codes, HTTPError, Response, Session, Timeout

from amplitude_python_sdk.common.utils import make_request, return_or_raise


@pytest.fixture
def fake_url():
    return "https://fake.researchrabbit"


def test_return_or_raise_failed_status():
    """Test a response with a failure status, and ensure that it correctly fails."""
    response = Response()
    response.status_code = 400
    response._content = b'{"error": "Failed to call Amplitude"}'
    with pytest.raises(HTTPError):
        return_or_raise(response)


def test_return_or_raise_success():
    """Test a response with a success status, and ensure that it does not fail."""
    response = Response()
    response.status_code = 200
    response._content = b'{"error": "Failed to call Amplitude"}'
    assert return_or_raise(response) == response


def test_make_request_timeout(requests_mock, fake_url):
    requests_mock.get(fake_url, exc=Timeout("Connection timed out."))
    session = Session()
    with pytest.raises(Timeout):
        make_request(session, "GET", fake_url)


def test_make_request_failure(requests_mock, fake_url):
    requests_mock.get(fake_url, status_code=status_codes.BAD_REQUEST, text="failure")
    session = Session()
    with pytest.raises(HTTPError):
        make_request(session, "GET", fake_url)


def test_make_request_success(requests_mock, fake_url):
    requests_mock.get(fake_url, text="success")
    session = Session()
    resp = make_request(session, "GET", fake_url)
    assert resp.text == "success"
