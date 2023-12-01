"""API requests and responses for the event endpoint."""
from datetime import datetime
from typing import List, Optional, Dict

from pydantic import (
    BaseModel,
    NonNegativeInt,
    PositiveInt,
)

from .base import Event
from .options import EventAPIOptions
from ....common.models import BaseAPIError


class UploadRequestBody(BaseModel):
    """
    Event API request model.
    See <https://developers.amplitude.com/docs/http-api-v2#uploadrequestbody>.
    """

    api_key: str
    events: List[Event]
    options: Optional[EventAPIOptions] = None

    class Config:
        json_encoders = {
            # Amplitude requires timestamps in millis, not seconds
            datetime: lambda v: int(v.timestamp() * 1000),
        }


class SuccessSummary(BaseModel):
    """
    Event API response model.
    See <https://developers.amplitude.com/docs/http-api-v2#200-response-successsummary>.
    """

    code: Optional[NonNegativeInt] = None
    events_ingested: Optional[NonNegativeInt] = None
    payload_size_bytes: Optional[NonNegativeInt] = None
    server_upload_time: Optional[PositiveInt] = None


class InvalidRequestError(BaseAPIError):
    """
    Event API error model.
    See <https://developers.amplitude.com/docs/http-api-v2#400-response-invalidrequesterror>.
    """

    missing_field: Optional[str] = None
    events_with_invalid_fields: Optional[Dict[str, List[NonNegativeInt]]] = None
    events_with_missing_fields: Optional[Dict[str, List[NonNegativeInt]]] = None


class PayloadTooLargeError(BaseAPIError):
    pass


class TooManyRequestsForDeviceError(BaseAPIError):
    eps_threshold: Optional[NonNegativeInt] = None
    throttled_devices: Optional[Dict[str, NonNegativeInt]] = None
    throttled_users: Optional[Dict[str, NonNegativeInt]] = None
    throttled_events: Optional[List[NonNegativeInt]] = None
