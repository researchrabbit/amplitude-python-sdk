import json

from amplitude_python_sdk.v1.models import UserProperties


def test_user_properties_serialization():
    set_fields = {"field1": True}
    prepend_fields = {"foo": "bar"}
    up = UserProperties(
        set_fields=set_fields, prepend_fields=prepend_fields, unset_fields=None
    )
    assert len(up.__fields_set__) == 3
    payload = up.payload
    assert len(payload) == 2
    assert set(payload.keys()) == {"$set", "$prepend"}
    assert payload["$set"] == set_fields
    assert payload["$prepend"] == prepend_fields
