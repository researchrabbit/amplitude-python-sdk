"""Client implementation for the Chart Annotations API."""
from typing import Optional

import requests

from ...common.clients import BasicAuthAPIClient
from ...common.utils import make_request
from ...v2 import routes
from ...v2.models.charts import (
    CreateChartAnnotationRequest,
    CreateChartAnnotationResponse,
    ListChartAnnotationsResponse,
    GetChartAnnotationResponse,
)


class ChartAnnotationsAPIClient(BasicAuthAPIClient):
    """
    See <https://developers.amplitude.com/docs/chart-annotations-api> for documentation.
    """

    def __init__(
        self,
        api_key: str,
        secret_key: str,
        chart_annotations_api_endpoint: str = "https://amplitude.com/api/2",
    ):
        super().__init__(api_key, secret_key)
        self.chart_annotations_api_endpoint = chart_annotations_api_endpoint

    def create(
        self,
        annotation: CreateChartAnnotationRequest,
        timeout: int = 5,
    ) -> CreateChartAnnotationResponse:
        """
        Create an annotation
        """

        resp = make_request(
            session=self.session,
            method="POST",
            url=self.chart_annotations_api_endpoint + routes.CHART_ANNOTATIONS_API,
            data=annotation.model_dump(exclude_none=True, exclude_unset=True),
            timeout=timeout,
        )
        return CreateChartAnnotationResponse.model_validate_json(resp.content)

    def list(self, timeout: int = 5) -> ListChartAnnotationsResponse:
        resp = self._get(timeout=timeout)
        return ListChartAnnotationsResponse.model_validate_json(resp.content)

    def get(self, annotation_id: int, timeout: int = 5) -> GetChartAnnotationResponse:
        resp = self._get(annotation_id, timeout)
        return GetChartAnnotationResponse.model_validate_json(resp.content)

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
