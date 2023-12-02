import requests

from amplitude_python_sdk.v1 import AmplitudeV1APIClient, Identification, UserProperties


def test_identify_request(mocker):
    mock_response = requests.Response()
    mock_response.status_code = 200
    mock_response._content = {}
    mocker.patch(
        "amplitude_python_sdk.v1.client.make_request",
        return_value=mock_response,
    )

    client = AmplitudeV1APIClient(api_key="fake")
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
    client.identify(ids=ids)
