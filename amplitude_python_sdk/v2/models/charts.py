"""
This module contains all models relating to the Amplitude V2 Chart Annotations API.

See <https://developers.amplitude.com/docs/chart-annotations-api> for documentation.
"""

from datetime import date
from typing import Optional

from pydantic import BaseModel  # pylint: disable=no-name-in-module


class ChartAnnotationsV2(BaseModel):  # pylint: disable=too-few-public-methods
    app_id: int
    date: date  # YYYY-MM-DD
    label: str
    chart_id: Optional[str] = None
    details: Optional[str] = None

