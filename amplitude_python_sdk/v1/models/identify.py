"""Models used to identify an individual user."""

import json
from typing import Any, Optional, Dict, List

from pydantic import BaseModel, Field

from ...common.models import DeviceInfo, LocationInfo, UserIdentifier


class UserProperties(BaseModel):
    """
    See <https://developers.amplitude.com/docs/identify-api#keys-for-the-identification-argument>
    for documentation.

    User properties are a set of arbitrary fields which can be nested JSON
    objects or simple key-value pairs.

    From the docs, here are the operations allowed:

    "This field supports the following user property operations:

    - $set (set the value of a property)
    - $setOnce (set the value of a property, prevent overriding the property value)
    - $add (add a numeric value to a numeric property)
    - $append and $prepend (append and prepend the value to a user property array)
    - $unset (remove a property)

    - $preInsert: This functionality will add the specified values to the
    beginning of the list of properties for the user property if the values do
    not already exist in the list. Can give a single value or an array of values.
    If a list is sent, the order of the list will be maintained.

    - $postInsert: This functionality will add the specified values to the end
    of the list of properties for the user property if the values do not
    already exist in the list. Can give a single value or an array of values.
    If a list is sent, the order of the list will be maintained.

    - $remove: This functionality will remove all instances of the values
    specified from the list. Can give a single value or an array of values.
    These should be keys in the dictionary where the values are the
    corresponding properties that you want to operate on."
    """

    set_fields: Optional[Dict[str, Any]] = Field(None, serialization_alias="$set")
    set_once_fields: Optional[Dict[str, Any]] = Field(
        None, serialization_alias="$setOnce"
    )
    add_fields: Optional[Dict[str, Any]] = Field(None, serialization_alias="$add")
    append_fields: Optional[Dict[str, Any]] = Field(None, serialization_alias="$append")
    prepend_fields: Optional[Dict[str, Any]] = Field(
        None, serialization_alias="$prepend"
    )
    unset_fields: Optional[Dict[str, Any]] = Field(None, serialization_alias="$unset")
    pre_insert_fields: Optional[Dict[str, Any]] = Field(
        None, serialization_alias="$preInsert"
    )
    post_insert_fields: Optional[Dict[str, Any]] = Field(
        None, serialization_alias="$postInsert"
    )
    remove_fields: Optional[Dict[str, Any]] = Field(None, serialization_alias="$remove")

    @property
    def payload(self) -> Dict[str, Any]:
        return self.model_dump(by_alias=True, exclude_none=True, exclude_unset=True)


class Identification(DeviceInfo, UserIdentifier, LocationInfo):
    """
    See <https://developers.amplitude.com/docs/identify-api#keys-for-the-identification-argument>
    for documentation.
    """

    language: Optional[str] = None
    paying: Optional[str] = None
    start_version: Optional[str] = None
    user_properties: Optional[UserProperties] = None

    @property
    def payload(self):
        base_dict = self.model_dump(
            exclude_none=True, exclude_unset=True, exclude={"user_properties"}
        )
        if self.user_properties:
            base_dict["user_properties"] = self.user_properties.payload
        return base_dict


class IdentifyAPIRequest(BaseModel):
    """
    Represents the API request made to the /identify API endpoint.
    """

    api_key: str
    identification: str

    @classmethod
    def from_ids(cls, api_key: str, ids: List[Identification]):
        return cls(
            api_key=api_key, identification=json.dumps([id.payload for id in ids])
        )
