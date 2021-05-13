import requests

from ...common.exceptions import AmplitudeAPIException
from ..models.event import (
    InvalidRequestError,
    PayloadTooLargeError,
    TooManyRequestsForDeviceError,
)


class InvalidRequestException(AmplitudeAPIException):
    @classmethod
    def from_response(cls, response: requests.Response):
        e = InvalidRequestError.parse_obj(response.json())
        return cls(e)


class PayloadTooLargeException(AmplitudeAPIException):
    @classmethod
    def from_response(cls, response: requests.Response):
        e = PayloadTooLargeError.parse_obj(response.json())
        return cls(e)


class TooManyRequestsForDeviceException(AmplitudeAPIException):
    @classmethod
    def from_response(cls, response: requests.Response):
        e = TooManyRequestsForDeviceError.parse_obj(response.json())
        return cls(e)
