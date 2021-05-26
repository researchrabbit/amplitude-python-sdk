"""
Client implementation for the Amplitude Releases API:
<https://developers.amplitude.com/docs/releases-api>
"""

from .. import routes
from ...common.clients import BasicAuthAPIClient
from ..models.releases import Release, CreateReleaseResponse
from ...common.utils import make_request


class ReleasesAPIClient(BasicAuthAPIClient):
    """
    See <https://developers.amplitude.com/docs/releases-api> for documentation.
    """

    def __init__(
        self,
        api_key: str,
        secret_key: str,
        releases_api_endpoint: str = "https://amplitude.com/api/2",
    ):
        super().__init__(api_key, secret_key)
        self.releases_api_endpoint = releases_api_endpoint

    def create(self, release: Release) -> CreateReleaseResponse:
        resp = make_request(
            self.session,
            "POST",
            routes.RELEASES_API,
            data=release.dict(exclude_none=True, exclude_unset=True),
        )
        return CreateReleaseResponse.parse_obj(resp.json())
