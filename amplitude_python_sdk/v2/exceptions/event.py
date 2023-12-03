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
        e = InvalidRequestError.model_validate_json(response.content)
        return cls(e)


class PayloadTooLargeException(AmplitudeAPIException):
    @classmethod
    def from_response(cls, response: requests.Response):
        e = PayloadTooLargeError.model_validate_json(response.content)
        return cls(e)


class TooManyRequestsForDeviceException(AmplitudeAPIException):
    @classmethod
    def from_response(cls, response: requests.Response):
        e = TooManyRequestsForDeviceError.model_validate_json(response.content)
        return cls(e)
