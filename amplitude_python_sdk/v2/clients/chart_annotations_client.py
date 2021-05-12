"""Client implementation for the Chart Annotations API."""
from typing import Optional

import requests

from amplitude_python_sdk.v2 import routes

from amplitude_python_sdk.v2.models.charts import ChartAnnotation
from amplitude_python_sdk.common.utils import make_request


class ChartAnnotationsAPIClient:
    """
    See <https://developers.amplitude.com/docs/chart-annotations-api> for documentation.
    """

    def __init__(
        self,
        api_key: str,
        secret_key: str,
        chart_annotations_api_endpoint: str = "https://amplitude.com/api/2",
    ):
        self.chart_annotations_api_endpoint = chart_annotations_api_endpoint
        self.session = requests.Session()
        self.session.auth = (api_key, secret_key)

    def create(
        self,
        annotation: ChartAnnotation,
        timeout: int = 5,
    ) -> requests.Response:
        """
        Create an annotation
        """

        return make_request(
            session=self.session,
            method="POST",
            url=self.chart_annotations_api_endpoint + routes.CHART_ANNOTATIONS_API,
            data=annotation.dict(exclude_none=True),
            timeout=timeout,
        )

    def list(self, timeout: int = 5) -> requests.Response:
        return self._get(timeout=timeout)

    def get(self, annotation_id: int, timeout: int = 5) -> requests.Response:
        return self._get(annotation_id, timeout)

    def _get(
        self,
        annotation_id: Optional[int] = None,
        timeout: int = 5,
    ) -> requests.Response:
        """
        Get all annotations or get annotation by id if provided
        """

        annotation_url_base = (
            self.chart_annotations_api_endpoint + routes.CHART_ANNOTATIONS_API
        )
        annotation_get_url = (
            f"{annotation_url_base}/{annotation_id}"
            if annotation_id
            else annotation_url_base
        )

        return make_request(
            session=self.session,
            method="GET",
            url=annotation_get_url,
            timeout=timeout,
        )
