"""
This module contains classes containing options for any
of the Amplitude API methods.
"""

from typing import Optional

from pydantic import BaseModel, PositiveInt  # pylint: disable=no-name-in-module


class V2EventAPIOptions(BaseModel):  # pylint: disable=too-few-public-methods
    """
    Options for the Amplitude V2 Event API.

    See <https://developers.amplitude.com/docs/http-api-v2#options> for more info.
    """

    # Defaults to minimum ID length of 5
    min_id_length: Optional[PositiveInt] = None
