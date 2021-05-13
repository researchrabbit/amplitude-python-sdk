"""Contains all exception classes used within this library."""
from abc import ABC

from amplitude_python_sdk.common.models import BaseAPIError


class AmplitudeAPIException(Exception, ABC):
    error: BaseAPIError

    def __init__(self, error: BaseAPIError):
        super().__init__()
        self.error = error
