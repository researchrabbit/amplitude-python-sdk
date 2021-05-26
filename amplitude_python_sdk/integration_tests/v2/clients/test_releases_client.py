from datetime import datetime, timedelta

import pytest

from amplitude_python_sdk.v2.clients.releases_client import ReleasesAPIClient
from amplitude_python_sdk.v2.models.releases import Release


@pytest.fixture(scope="module")
def client(test_api_key: str, test_secret_key: str) -> ReleasesAPIClient:
    return ReleasesAPIClient(api_key=test_api_key, secret_key=test_secret_key)


@pytest.fixture(scope="module")
def release():
    return Release(
        version=f"test_version_{int(datetime.now().timestamp())}",
        release_start=datetime.now(),
        release_end=datetime.now() + timedelta(days=30),
        title="test release 1",
        description="this is a description",
        platforms=["Android", "iOS", "Web"],
        created_by="test_user",
    )


def test_create_release_successful(client: ReleasesAPIClient, release: Release):
    response_data = client.create(release)
    assert response_data.success is True
    assert response_data.release is not None
    assert response_data.release.version == release.version
    assert response_data.release.title == release.title
    assert response_data.release.platforms == release.platforms
