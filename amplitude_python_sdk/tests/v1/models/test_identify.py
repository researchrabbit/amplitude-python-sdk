import json

from amplitude_python_sdk.v1.models import (
    Identification,
    IdentifyAPIRequest,
    UserProperties,
)


def test_user_properties_serialization():
    set_fields = {"field1": True}
    prepend_fields = {"foo": "bar"}
    up = UserProperties(
        set_fields=set_fields, prepend_fields=prepend_fields, unset_fields=None
    )
    assert len(up.model_fields_set) == 3
    payload = up.payload
    assert len(payload) == 2
    assert set(payload.keys()) == {"$set", "$prepend"}
    assert payload["$set"] == set_fields
    assert payload["$prepend"] == prepend_fields


def test_identification_payload():
    i = Identification(user_id="user_id_example", language="en", paying="False")
    payload = i.payload
    assert len(payload) == 3
    assert set(payload.keys()) == {"language", "paying", "user_id"}
    assert "user_properties" not in payload


def test_identification_user_properties_payload():
    set_fields = {"field1": True}
    prepend_fields = {"foo": "bar"}
    up = UserProperties(
        set_fields=set_fields, prepend_fields=prepend_fields, unset_fields=None
    )
    assert len(up.model_fields_set) == 3

    i = Identification(
        user_id="user_id_example", language="en", paying="False", user_properties=up
    )
    assert len(i.model_fields_set) == 4

    payload = i.payload
    assert len(payload) == 4
    assert set(payload.keys()) == {"language", "paying", "user_id", "user_properties"}

    user_properties_serialized = payload["user_properties"]
    assert len(user_properties_serialized) == 2
    assert set(user_properties_serialized.keys()) == {"$set", "$prepend"}
    assert user_properties_serialized["$set"] == set_fields
    assert user_properties_serialized["$prepend"] == prepend_fields


def test_identify_api_request_from_ids():
    set_fields = {"field1": True}
    prepend_fields = {"foo": "bar"}
    up = UserProperties(
        set_fields=set_fields, prepend_fields=prepend_fields, unset_fields=None
    )
    assert len(up.model_fields_set) == 3

    ids = [
        Identification(
            user_id=f"user_id_example_{i}",
            language="en",
            paying="False",
            user_properties=up,
        )
        for i in range(10)
    ]

    request = IdentifyAPIRequest.from_ids(api_key="fake", ids=ids)
    deserialized = json.loads(
        request.identification
    )  # Ensure that ids can be read back as JSON
    assert len(deserialized) == 10
    for i, ident in enumerate(deserialized):
        assert ident["user_id"] == f"user_id_example_{i}"
        assert ident["language"] == "en"
        assert ident["paying"] == "False"

        user_properties_serialized = ident["user_properties"]
        assert len(user_properties_serialized) == 2
        assert set(user_properties_serialized.keys()) == {"$set", "$prepend"}
        assert user_properties_serialized["$set"] == set_fields
        assert user_properties_serialized["$prepend"] == prepend_fields
