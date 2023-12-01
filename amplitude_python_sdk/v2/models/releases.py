"""
Models used to interact with the Amplitude Releases API:
<https://developers.amplitude.com/docs/releases-api>
"""

import json
from datetime import datetime
from typing import Union, Optional, List

from pydantic import BaseModel


class Release(BaseModel):
    """
    Request body for creating a release.

    See <https://developers.amplitude.com/docs/releases-api#creating-releases>
    for API documentation.
    """

    version: Union[str, int, float]
    release_start: datetime
    release_end: Optional[datetime] = None
    title: str
    description: Optional[str] = None
    platforms: Optional[List[str]] = None
    created_by: Optional[str] = None
    chart_visibility: bool = True

    def dict(self, *args, **kwargs):
        base_dict = super().dict(*args, **kwargs)
        if self.created_by:
            # Delete created_by top-level key and nest it under params object instead.
            base_dict.pop("created_by", None)
            base_dict["params"] = json.dumps({"created_by": self.created_by})
        return base_dict

    class Config:
        json_encoders = {
            # The Releases API requires the dates to be passed in exactly this string format.
            datetime: lambda v: v.strftime("%Y-%m-%d %H:%M:%S"),
        }


class ReleaseResponseMetadata(BaseModel):
    """
    Object metadata that comes back from Amplitude after creating a new release.

    See <https://developers.amplitude.com/docs/releases-api#example-response>.
    """

    last_modified: datetime
    last_modified_by: str
    created: datetime
    created_by: str


class ReleaseResponse(Release):
    """
    Newly created release object that comes back from Amplitude after creation succeeds.

    See <https://developers.amplitude.com/docs/releases-api#example-response>.
    """

    id: str
    app_id: int
    org_id: int
    type: str
    params: Optional[ReleaseResponseMetadata] = None


class CreateReleaseResponse(BaseModel):
    """
    HTTP Response coming from the releases API.

    Contains a success status flag + created release object.
    """

    success: bool
    release: ReleaseResponse
