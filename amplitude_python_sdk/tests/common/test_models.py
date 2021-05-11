import pytest
from pydantic import ValidationError

from amplitude_python_sdk.common.models import UserIdentifier


def test_event_identifier_validate_user_device_id_invalid():
    with pytest.raises(ValidationError):
        ident = UserIdentifier()


def test_event_identifier_validate_user_device_id_valid():
    ident = UserIdentifier(user_id="foo", device_id="bar")
    ident2 = UserIdentifier(user_id="uid_only")
    ident3 = UserIdentifier(device_id="did_only")
