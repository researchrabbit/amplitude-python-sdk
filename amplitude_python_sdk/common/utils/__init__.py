"""This package contains utility functions used in both V1 and V2 SDK methods."""

import requests


def return_or_raise(
    response: requests.Response,
):  # pylint: disable=missing-function-docstring
    response.raise_for_status()
    return response
