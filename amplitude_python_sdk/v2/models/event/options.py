"""Contains option classes for any of the Amplitude API methods."""

from pydantic import BaseModel, PositiveInt


class EventAPIOptions(BaseModel):
    """
    Options for the Amplitude V2 Event API.

    See <https://developers.amplitude.com/docs/http-api-v2#options> for more info.
    """

    min_id_length: PositiveInt
