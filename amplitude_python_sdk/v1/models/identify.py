"""Models used to identify an individual user."""

from typing import Any, Optional, Dict, List

from pydantic import BaseModel, Field, Json  # pylint: disable=no-name-in-module

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

    set_fields: Optional[Dict[str, Any]] = Field(None, json_name="$set")
    set_once_fields: Optional[Dict[str, Any]] = Field(None, json_name="$setOnce")
    add_fields: Optional[Dict[str, Any]] = Field(None, json_name="$add")
    append_fields: Optional[Dict[str, Any]] = Field(None, json_name="$append")
    prepend_fields: Optional[Dict[str, Any]] = Field(None, json_name="$prepend")
    unset_fields: Optional[Dict[str, Any]] = Field(None, json_name="$unset")
    pre_insert_fields: Optional[Dict[str, Any]] = Field(None, json_name="$preInsert")
    post_insert_fields: Optional[Dict[str, Any]] = Field(None, json_name="$postInsert")
    remove_fields: Optional[Dict[str, Any]] = Field(None, json_name="$remove")

    @property
    def payload(self):  # pylint: disable=missing-function-docstring
        """
        HACK: This is done to work around the lack of a dump_alias function
        in Pydantic at the moment to change the JSON output field names.

        In a future release when we can add aliases for JSON output, we
        should be able to remove this function and set the aliases directly
        on the field definition. Then we can just call .json() directly.

        See https://github.com/samuelcolvin/pydantic/issues/624 for details.
        """
        output = {}
        schema = self.schema()
        for field_name in self.__fields_set__:
            field_props = schema["properties"][field_name]
            field_value = getattr(self, field_name)
            if field_value is not None:
                output[field_props["json_name"]] = field_value
        return output


class Identification(
    DeviceInfo, EventIdentifier, LocationInfo
):  # pylint: disable=too-few-public-methods
    """
    See <https://developers.amplitude.com/docs/identify-api#keys-for-the-identification-argument>
    for documentation.
    """

    language: Optional[str] = None
    paying: Optional[str] = None
    start_version: Optional[str] = None
    user_properties: Optional[UserProperties] = None


class IdentificationList(BaseModel):  # pylint: disable=too-few-public-methods
    """Wrapper class representing a list of Identification objects for JSON serialization."""

    __root__: List[Identification] = []


class IdentifyAPIRequest(BaseModel):  # pylint: disable=too-few-public-methods
    """
    Represents the API request made to the /identify API endpoint.
    """

    api_key: str
    identification: Json
