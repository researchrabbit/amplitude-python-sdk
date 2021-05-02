"""Models used to identify an individual user."""

from typing import Optional, Dict, Any

from pydantic import BaseModel  # pylint: disable=no-name-in-module

from ...common.models import DeviceInfo, LocationInfo, EventIdentifier


class UserProperties(BaseModel):  # pylint: disable=too-few-public-methods
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

    set_fields: Optional[Dict[str, Any]] = None
    set_once_fields: Optional[Dict[str, Any]] = None
    add_fields: Optional[Dict[str, Any]] = None
    append_fields: Optional[Dict[str, Any]] = None
    prepend_fields: Optional[Dict[str, Any]] = None
    unset_fields: Optional[Dict[str, Any]] = None
    pre_insert_fields: Optional[Dict[str, Any]] = None
    post_insert_fields: Optional[Dict[str, Any]] = None
    remove_fields: Optional[Dict[str, Any]] = None

    @property
    def payload(self):
        """
        Converts the class fields into a request payload
        that the Amplitude API will accept.
        """
        output = {}
        if self.set_fields:
            output["$set"] = self.set_fields
        if self.set_once_fields:
            output["$setOnce"] = self.set_once_fields
        if self.add_fields:
            output["$add"] = self.add_fields
        if self.append_fields:
            output["$append"] = self.append_fields
        if self.prepend_fields:
            output["$prepend"] = self.prepend_fields
        if self.unset_fields:
            output["$unset"] = self.unset_fields
        if self.pre_insert_fields:
            output["$preInsert"] = self.unset_fields
        if self.post_insert_fields:
            output["$postInsert"] = self.unset_fields
        if self.remove_fields:
            output["$remove"] = self.unset_fields
        return output


class Identification(DeviceInfo, EventIdentifier, LocationInfo):
    """
    See <https://developers.amplitude.com/docs/identify-api#keys-for-the-identification-argument>
    for documentation.
    """

    language: Optional[str] = None
    paying: Optional[str] = None
    start_version: Optional[str] = None
    user_properties: Optional[UserProperties] = None

    @property
    def payload(self) -> dict:
        """
        Generates the payload (as a Python dictionary) required by the
        Amplitude API for identifying a user.
        """
        base_dict = self.dict(exclude={"user_properties"}, exclude_none=True)
        if self.user_properties:
            base_dict["user_properties"] = self.user_properties.payload
        return base_dict
