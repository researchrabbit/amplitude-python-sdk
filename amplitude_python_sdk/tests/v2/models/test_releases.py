import json
from datetime import datetime, timedelta

import pytest

from amplitude_python_sdk.v2.models.releases import Release


@pytest.fixture
def release() -> Release:
    return Release(
        version="test_version",
        release_start=datetime.now(),
        release_end=datetime.now() + timedelta(days=30),
        title="test release 1",
        created_by="test_user",
    )


def test_release_model_dump(release: Release):
    d = release.model_dump(exclude_none=True, exclude_unset=True)
    assert len(d) == 6
    assert d.get("version") == release.version
    assert d.get("release_start") == release.format_datetime(release.release_start)
    assert d.get("release_end") == release.format_datetime(release.release_end)
    assert d.get("title") == release.title
    assert d.get("chart_visibility") == release.chart_visibility
    assert "created_by" not in d
    assert d.get("params") is not None
    assert isinstance(d.get("params"), str)

    params_dict = json.loads(d.get("params"))
    assert isinstance(params_dict, dict)
    assert len(params_dict) == 1
    assert params_dict.get("created_by") == release.created_by
