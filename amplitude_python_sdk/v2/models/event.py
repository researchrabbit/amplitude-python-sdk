"""
This module contains all models relating to the Amplitude V2 HTTP Event API.

See <https://developers.amplitude.com/docs/http-api-v2> for documentation.
"""

from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel  # pylint: disable=no-name-in-module

from ...common.models import DeviceInfo, LocationInfo, UserIdentifier
from .options import EventAPIOptions


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


class Event(
    DeviceInfo, EventIdentifiers, EventLocationData, UserIdentifier
):  # pylint: disable=too-few-public-methods
    """
    See <https://developers.amplitude.com/docs/http-api-v2#keys-for-the-event-argument>
    for documentation.
    """

    event_type: str
    time: Optional[datetime] = None
    event_properties: Optional[Dict[str, Any]] = None
    user_properties: Optional[Dict[str, Any]] = None
    groups: Optional[Dict[str, Any]] = None
    app_version: Optional[str] = None


class EventAPIRequest(BaseModel):  # pylint: disable=too-few-public-methods
    api_key: str
    events: List[Event]
    options: Optional[EventAPIOptions] = None
