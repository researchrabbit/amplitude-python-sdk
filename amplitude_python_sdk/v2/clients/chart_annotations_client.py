"""Client implementation for the Chart Annotations API."""
from typing import Optional

import requests

from amplitude_python_sdk.v2 import routes

from amplitude_python_sdk.v2.models.charts import ChartAnnotationsV2
from amplitude_python_sdk.common.exceptions import AmplitudeAPIException
from amplitude_python_sdk.common.utils import return_or_raise


class ChartAnnotationsAPIClient:  # pylint: disable=too-few-public-methods
    """
    See <https://developers.amplitude.com/docs/chart-annotations-api> for documentation.
    """

    def __init__(
        self,
        api_key: str,
        secret_key: str,
        chart_annotations_api_endpoint: str = "https://amplitude.com/api/2"
    ):
        self.api_key = api_key
        self.secret_key = secret_key
        self.chart_annotations_api_endpoint = chart_annotations_api_endpoint

    def chart_annotations_post(
        self, annotation: ChartAnnotationsV2, timeout: int = 5,
    ) -> requests.Response:
        """
        Create an annotation
        """

        try:
            resp = requests.post(
                url=self.chart_annotations_api_endpoint + routes.CHART_ANNOTATIONS_API,
                auth=(self.api_key, self.secret_key),
                data=annotation.dict(exclude_none=True),
                timeout=timeout
            )
            return return_or_raise(resp)
        except requests.exceptions.Timeout as exc:
            raise AmplitudeAPIException() from exc

    def chart_annotations_get(
        self, annotation_id: Optional[str] = None, timeout: int = 5,
    ) -> requests.Response:
        """
        Get all annotations or Get annotation by id if provided
        """
        annotation_get_url = self.chart_annotations_api_endpoint + routes.CHART_ANNOTATIONS_API
        if annotation_id:
            annotation_get_url += '/' + annotation_id

        try:
            resp = requests.get(
                url=annotation_get_url,
                auth=(self.api_key, self.secret_key),
                timeout=timeout
            )
            return return_or_raise(resp)
        except requests.exceptions.Timeout as exc:
            raise AmplitudeAPIException() from exc
