"""Contains utility functions used in both V1 and V2 SDK methods."""

import requests

from .exceptions import AmplitudeAPIException


def return_or_raise(
    response: requests.Response,
):  # pylint: disable=missing-function-docstring
    try:
        response.raise_for_status()
    except requests.HTTPError as exc:
        raise AmplitudeAPIException(response.text) from exc

    return response
