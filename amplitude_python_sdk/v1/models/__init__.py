"""
This package contains all Pydantic models used for the Amplitude V1 API
requests and responses.
"""

from .identify import Identification, IdentifyAPIRequest, UserProperties

__all__ = ["Identification", "IdentifyAPIRequest", "UserProperties"]
