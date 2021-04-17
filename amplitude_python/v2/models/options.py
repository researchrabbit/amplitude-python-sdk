"""
This module contains classes containing options for any
of the Amplitude API methods.
"""

from typing import Optional

from pydantic import BaseModel, validator  # pylint: disable=no-name-in-module


class V2EventAPIOptions(BaseModel):  # pylint: disable=too-few-public-methods
    """
    Options for the Amplitude V2 Event API.

    See <https://developers.amplitude.com/docs/http-api-v2#options> for more info.
    """

    min_id_length: Optional[int] = None

    @classmethod
    @validator("min_id_length")
    def must_be_positive(
        cls, v
    ):  # pylint: disable=invalid-name,missing-function-docstring
        if v <= 0:
            raise ValueError("min_id_length must be a positive number")
        return v
