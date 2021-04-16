from typing import Optional, Dict

from pydantic import BaseModel, root_validator


class UserProperties(BaseModel):
    set_fields: Optional[Dict[str, str]] = None
    set_once_fields: Optional[Dict[str, str]] = None
    add_fields: Optional[Dict[str, str]] = None
    append_fields: Optional[Dict[str, str]] = None
    prepend_fields: Optional[Dict[str, str]] = None
    unset_fields: Optional[Dict[str, str]] = None

    @property
    def payload(self):
        output = {}
        if self.set_fields:
            output['$set'] = self.set_fields
        if self.set_once_fields:
            output['$setOnce'] = self.set_once_fields
        if self.add_fields:
            output['$add'] = self.add_fields
        if self.append_fields:
            output['$append'] = self.append_fields
        if self.prepend_fields:
            output['$prepend'] = self.prepend_fields
        if self.unset_fields:
            output['$unset'] = self.unset_fields
        return output


class DeviceInfo(BaseModel):
    """
    See https://developers.amplitude.com/docs/identify-api#keys-for-the-identification-argument:

    "These fields (platform, os_name, os_version, device_brand, device_manufacturer, device_model, and carrier) must all
    be updated together.

    Setting any of these fields will automatically reset all of the other property values to null if they are not also
    explicitly set on the same identify call. All property values will otherwise persist to a subsequent event if the
    values are not changed to a different string or if all values are passed as null.

    Amplitude will attempt to use device_brand, device_manufacturer, and device_model to map the corresponding
    device type."
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
    See https://developers.amplitude.com/docs/identify-api#keys-for-the-identification-argument:

    "These fields (country, region, city, DMA) must all be updated together.
    Setting any of these fields will automatically reset all of the others
    if they are not also set on the same identify call."
    """
    country: Optional[str] = None
    region: Optional[str] = None
    city: Optional[str] = None
    dma: Optional[str] = None


class Identification(DeviceInfo, LocationInfo):
    user_id: Optional[str] = None
    device_id: Optional[str] = None
    language: Optional[str] = None
    paying: Optional[str] = None
    start_version: Optional[str] = None
    user_properties: Optional[UserProperties] = None

    @classmethod
    @root_validator
    def check_user_id_or_device_id(cls, values):
        uid, did = values.get('user_id'), values.get('device_id')
        if not (uid or did):
            raise ValueError('Must provide at least one of user_id and device_id')
        return values

    @property
    def payload(self):
        base_dict = self.dict(exclude={'user_properties'}, exclude_none=True)
        if self.user_properties:
            base_dict['user_properties'] = self.user_properties.payload
        return base_dict
