"""
This module contains all models relating to the Amplitude V2 Chart Annotations API.

See <https://developers.amplitude.com/docs/chart-annotations-api> for documentation.
"""
from abc import ABC
from datetime import date as date_type
from typing import Optional, List

from pydantic import BaseModel


class ChartAnnotationBase(BaseModel, ABC):
    date: date_type
    label: str
    details: Optional[str] = None


class ChartAnnotation(ChartAnnotationBase):
    id: int


class CreateChartAnnotationRequest(ChartAnnotationBase):
    """
    Chart annotation request body, used in Amplitude to denote chronological events.
    """

    # Amplitude project ID that the annotation should be added to.
    app_id: int
    # If chart_id is not supplied, the annotation is global.
    chart_id: Optional[str] = None


class ChartAnnotationResponseBase(BaseModel, ABC):
    annotation: Optional[ChartAnnotation] = None


class GetChartAnnotationResponse(ChartAnnotationResponseBase):
    pass


class CreateChartAnnotationResponse(ChartAnnotationResponseBase):
    success: Optional[bool] = None


class ListChartAnnotationsResponse(BaseModel):
    data: List[ChartAnnotation]
