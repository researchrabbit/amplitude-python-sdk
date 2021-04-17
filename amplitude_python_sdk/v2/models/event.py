"""
This module contains all models relating to the Amplitude V2 HTTP Event API.

See <https://developers.amplitude.com/docs/http-api-v2> for documentation.
"""

from datetime import datetime
from typing import Optional, Any, Dict

from pydantic import BaseModel, root_validator  # pylint: disable=no-name-in-module

from ...common.models import DeviceInfo, LocationInfo
from ...common.utils.model_validators import check_user_id_or_device_id


class MobileIdentifiers(BaseModel):  # pylint: disable=too-few-public-methods
    """
    See <https://developers.amplitude.com/docs/http-api-v2#keys-for-the-event-argument>
    for documentation.

    The fields in this class represent mobile advertising and vendor identifiers
    from Android and iOS devices.
    """

    idfa: Optional[str] = None
    idfv: Optional[str] = None
    adid: Optional[str] = None
    android_id: Optional[str] = None


class EventIdentifiers(BaseModel):  # pylint: disable=too-few-public-methods
    """
    Represents a set of identifiers that can be used to uniquely identify an
    event, session, or insert attempt for idempotency.
    """

    event_id: Optional[int] = None
    session_id: Optional[int] = None
    insert_id: Optional[str] = None


class EventLocationData(LocationInfo):  # pylint: disable=too-few-public-methods
    """
    Extends LocationInfo and adds fields representing the latitude/longitude of a
    user and their IP address.
    """

    location_lat: Optional[float] = None
    location_lng: Optional[float] = None
    ip: Optional[str] = None


class EventV2(
    DeviceInfo, EventIdentifiers, EventLocationData
):  # pylint: disable=too-few-public-methods
    """
    See <https://developers.amplitude.com/docs/http-api-v2#keys-for-the-event-argument>
    for documentation.
    """

    event_type: str
    user_id: Optional[str] = None
    device_id: Optional[str] = None
    time: Optional[datetime] = None
    event_properties: Optional[Dict[str, Any]] = None
    user_properties: Optional[Dict[str, Any]] = None
    groups: Optional[Dict[str, Any]] = None
    app_version: Optional[str] = None

    @classmethod
    @root_validator
    def validate_user_device_id(
        cls, values
    ):  # pylint: disable=missing-function-docstring
        return check_user_id_or_device_id(values)
