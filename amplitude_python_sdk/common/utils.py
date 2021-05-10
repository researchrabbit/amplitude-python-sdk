"""Contains utility functions used in both V1 and V2 SDK methods."""

import requests

from .exceptions import AmplitudeAPIException


def return_or_raise(response: requests.Response):
    try:
        response.raise_for_status()
    except requests.HTTPError as exc:
        raise AmplitudeAPIException(response.text) from exc

    return response


def make_request(
    session: requests.Session, method: str, url, **kwargs
) -> requests.Response:
    """
    Make a request using a session object, and return a wrapped exception
    if it fails for any reason.
    """
    try:
        resp = session.request(method, url, **kwargs)
        return return_or_raise(resp)
    except requests.exceptions.RequestException as exc:
        raise AmplitudeAPIException() from exc
