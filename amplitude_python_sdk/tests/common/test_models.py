import pytest
from pydantic import ValidationError

from amplitude_python_sdk.common.models import UserIdentifier


def test_event_identifier_validate_user_device_id_invalid():
    with pytest.raises(ValidationError):
        UserIdentifier()


def test_event_identifier_validate_user_device_id_valid():
    UserIdentifier(user_id="foo", device_id="bar")
    UserIdentifier(user_id="uid_only")
    UserIdentifier(device_id="did_only")
