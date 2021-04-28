"""Client implementation for the Amplitude V2 Annotations API."""

from typing import Optional, Dict, Any

import requests

from .models.charts import ChartAnnotationsV2
from ..common.exceptions import AmplitudeAPIException
from ..common.utils import return_or_raise


class ChartAnnotationsApiClient:  # pylint: disable=too-few-public-methods
    """
    See <https://developers.amplitude.com/docs/chart-annotations-api> for documentation.
    """

    def __init__(
        self, api_key: str,
        api_endpoint: str = "https://api2.amplitude.com/2/annotations",
        annotation_id: Optional[str] = None
    ):
        self.api_key = api_key
        self.api_endpoint = api_endpoint
        self.annotation_id = annotation_id

    def _construct_chart_request_data(
        self, annotation: ChartAnnotationsV2
    ) -> Dict[str, Any]:
        """
        Convert ChartAnnotationsV2 model to dictionary payload for create annotation post request
        """

        req_data = {
            "api_key": self.api_key,
            "annotation": annotation.dict(exclude_none=True),
        }
        return req_data

    def _chart_annotations_post(
        self, req_data: Dict[str, Any], timeout: int = 5,
    ) -> requests.Response:
        """
        Create an annotation
        """

        try:
            resp = requests.post(
                url=self.api_endpoint, json=req_data, timeout=timeout
            )
            return return_or_raise(resp)
        except requests.exceptions.Timeout as exc:
            raise AmplitudeAPIException() from exc

    def _chart_annotations_get_all(
        self, timeout: int = 5,
    ) -> requests.Response:
        """
        Get all annotations
        """

        try:
            resp = requests.get(url=self.api_endpoint, timeout=timeout)
            return return_or_raise(resp)
        except requests.exceptions.Timeout as exc:
            raise AmplitudeAPIException() from exc

    def _chart_annotations_get_by_id(
        self, annotation_id: Optional[str], timeout: int = 5,
    ) -> requests.Response:
        """
        Get annotation by id
        """

        try:
            resp = requests.get(url=self.api_endpoint + "/" + annotation_id, timeout=timeout)
            return return_or_raise(resp)
        except requests.exceptions.Timeout as exc:
            raise AmplitudeAPIException() from exc

