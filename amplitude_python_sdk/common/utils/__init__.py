"""This package contains utility functions used in both V1 and V2 SDK methods."""

import requests

from ..exceptions import AmplitudeAPIException

__all__ = ["return_or_raise"]


def return_or_raise(
    response: requests.Response,
):  # pylint: disable=missing-function-docstring
    try:
        response.raise_for_status()
    except requests.HTTPError as exc:
        raise AmplitudeAPIException(response.json()) from exc

    return response
