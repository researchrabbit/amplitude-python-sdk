"""Contains common models used in both V1 and V2 APIs."""
from typing import Optional

from pydantic import (
    BaseModel,
    model_validator,
    PositiveInt,
)


class UserIdentifier(BaseModel):
    """
    Most events in Amplitude are tied to either a user ID or a device ID
    (you can provide both, but at least 1 must be present).
    """

    user_id: Optional[str] = None
    device_id: Optional[str] = None

    @model_validator(mode="before")
    def validate_user_device_id(cls, values: dict):
        """
        At least one of device_id and user_id MUST be set according to the
        Amplitude documentation. This validator enforces that requirement.
        """
        uid, did = values.get("user_id"), values.get("device_id")
        if not (uid or did):
            raise ValueError("Must provide at least one of user_id and device_id")

        return values


class DeviceInfo(BaseModel):
    """
    See <https://developers.amplitude.com/docs/identify-api#keys-for-the-identification-argument>:

    "These fields (platform, os_name, os_version, device_brand,
    device_manufacturer, device_model, and carrier) must all be updated
    together.

    Setting any of these fields will automatically reset all of the other
    property values to null if they are not also explicitly set on the same
    identify call.

    All property values will otherwise persist to a subsequent event
    if the values are not changed to a different string
    or if all values are passed as null.

    Amplitude will attempt to use device_brand, device_manufacturer,
    and device_model to map the corresponding device type."
    """

    platform: Optional[str] = None
    os_name: Optional[str] = None
    os_version: Optional[str] = None
    device_brand: Optional[str] = None
    device_manufacturer: Optional[str] = None
    device_model: Optional[str] = None
    carrier: Optional[str] = None


class LocationInfo(BaseModel):
    """
    See <https://developers.amplitude.com/docs/identify-api#keys-for-the-identification-argument>:

    "These fields (country, region, city, DMA) must all be updated together.
    Setting any of these fields will automatically reset all of the others
    if they are not also set on the same identify call."
    """

    country: Optional[str] = None
    region: Optional[str] = None
    city: Optional[str] = None
    dma: Optional[str] = None


class BaseAPIError(BaseModel):
    code: Optional[PositiveInt] = None
    error: Optional[str] = None
