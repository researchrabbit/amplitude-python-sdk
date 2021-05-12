"""Contains utility functions used in both V1 and V2 SDK methods."""

import requests


def return_or_raise(response: requests.Response):
    response.raise_for_status()
    return response


def make_request(
    session: requests.Session, method: str, url, **kwargs
) -> requests.Response:
    """
    Make a request using a session object, and return a wrapped exception
    if it fails for any reason.
    """
    resp = session.request(method, url, **kwargs)
    return return_or_raise(resp)
