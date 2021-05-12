from pydantic import parse_obj_as
import requests

from ...common.exceptions import AmplitudeAPIException
from ..models.event import (
    InvalidRequestError,
    PayloadTooLargeError,
    TooManyRequestsForDeviceError,
)


class InvalidRequestException(AmplitudeAPIException):
    error: InvalidRequestError

    def __init__(self, error: InvalidRequestError):
        self.error = error

    @classmethod
    def from_response(cls, response: requests.Response):
        e = parse_obj_as(InvalidRequestError, response.json())
        return cls(e)


class PayloadTooLargeException(AmplitudeAPIException):
    error: PayloadTooLargeError

    @classmethod
    def from_response(cls, response: requests.Response):
        e = parse_obj_as(PayloadTooLargeError, response.json())
        return cls(e)


class TooManyRequestsForDeviceException(AmplitudeAPIException):
    error: TooManyRequestsForDeviceError

    @classmethod
    def from_response(cls, response: requests.Response):
        e = parse_obj_as(TooManyRequestsForDeviceError, response.json())
        return cls(e)
