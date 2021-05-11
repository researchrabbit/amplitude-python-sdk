"""Client implementation for the Chart Annotations API."""
from typing import Optional

import requests

from amplitude_python_sdk.v2 import routes

from amplitude_python_sdk.v2.models.charts import ChartAnnotations
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
        annotation: ChartAnnotations,
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

    def get(
        self,
        annotation_id: Optional[str] = None,
        timeout: int = 5,
    ) -> requests.Response:
        """
        Get all annotations or Get annotation by id if provided
        """

        annotation_get_url = (
            self.chart_annotations_api_endpoint + routes.CHART_ANNOTATIONS_API
        )
        if annotation_id:
            annotation_get_url += "/" + annotation_id

        return make_request(
            session=self.session,
            method="GET",
            url=annotation_get_url,
            timeout=timeout,
        )
