import pytest
from pydantic import ValidationError

from amplitude_python_sdk.common.models import EventIdentifier


def test_event_identifier_validate_user_device_id_invalid():
    with pytest.raises(ValidationError):
        ident = EventIdentifier()


def test_event_identifier_validate_user_device_id_valid():
    ident = EventIdentifier(user_id="foo", device_id="bar")
    ident2 = EventIdentifier(user_id="uid_only")
    ident3 = EventIdentifier(device_id="did_only")
