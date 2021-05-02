"""Test file for the functions in the utils package."""

import pytest
from requests import Response

from amplitude_python_sdk.common.utils import return_or_raise
from amplitude_python_sdk.common.exceptions import AmplitudeAPIException


def test_return_or_raise_failed_status():
    """Test a response with a failure status, and ensure that it correctly fails."""
    response = Response()
    response.status_code = 400
    response._content = (  # pylint: disable=protected-access
        b'{"error": "Failed to call Amplitude"}'
    )
    with pytest.raises(AmplitudeAPIException):
        return_or_raise(response)


def test_return_or_raise_success():
    """Test a response with a success status, and ensure that it does not fail."""
    response = Response()
    response.status_code = 200
    response._content = (  # pylint: disable=protected-access
        b'{"error": "Failed to call Amplitude"}'
    )
    assert return_or_raise(response) == response
