from datetime import datetime, timedelta

import pytest

from amplitude_python_sdk.v2 import routes
from amplitude_python_sdk.v2.clients.releases_client import ReleasesAPIClient
from amplitude_python_sdk.v2.models.releases import (
    Release,
    CreateReleaseResponse,
    ReleaseResponse,
)


@pytest.fixture
def release():
    return Release(
        version="test_version",
        release_start=datetime.now(),
        release_end=datetime.now() + timedelta(days=30),
        title="test release 1",
        created_by="krishnan_test_user",
    )


@pytest.fixture
def releases_client() -> ReleasesAPIClient:
    return ReleasesAPIClient(
        api_key="apikey",
        secret_key="secretkey",
        releases_api_endpoint="https://fake.researchrabbit",
    )


@pytest.fixture
def release_response() -> ReleaseResponse:
    return ReleaseResponse(
        version="x.y.z",
        release_start=datetime.now().replace(microsecond=0),
        release_end=(datetime.now() + timedelta(days=30)).replace(microsecond=0),
        title="test release",
        type="integration",
        org_id=21,
        app_id=3,
        platforms=["Android", "iOS", "Web"],
        id="o15ux9n",
    )


@pytest.fixture
def create_release_response(release_response: ReleaseResponse) -> CreateReleaseResponse:
    return CreateReleaseResponse(success=True, release=release_response)


def test_create_success(
    requests_mock,
    release: Release,
    create_release_response: CreateReleaseResponse,
    releases_client: ReleasesAPIClient,
):
    requests_mock.post(
        releases_client.releases_api_endpoint + routes.RELEASES_API,
        json=create_release_response.model_dump(),
    )

    response = releases_client.create(release)
    assert response == create_release_response
