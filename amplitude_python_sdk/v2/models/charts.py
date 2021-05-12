"""
This module contains all models relating to the Amplitude V2 Chart Annotations API.

See <https://developers.amplitude.com/docs/chart-annotations-api> for documentation.
"""

from datetime import date as date_type
from typing import Optional

from pydantic import BaseModel  # pylint: disable=no-name-in-module


class ChartAnnotation(BaseModel):
    """
    Chart annotation entity, used in Amplitude to denote chronological events.
    """

    app_id: int
    date: date_type
    label: str
    chart_id: Optional[str] = None
    details: Optional[str] = None
