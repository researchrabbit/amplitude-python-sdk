"""This package contains all logic relating to the Amplitude V1 API."""

from .client import AmplitudeV1APIClient
from .models.identify import Identification, UserProperties

__all__ = ["AmplitudeV1APIClient", "Identification", "UserProperties"]
