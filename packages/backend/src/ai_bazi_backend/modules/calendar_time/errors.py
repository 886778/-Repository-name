"""Typed failures for deterministic calendar and time processing."""

from dataclasses import dataclass
from enum import StrEnum


class CalendarTimeErrorCode(StrEnum):
    UNSUPPORTED_CALENDAR = "unsupported_calendar"
    DATE_PRECISION_INSUFFICIENT = "date_precision_insufficient"
    INVALID_CALENDAR_DATE = "invalid_calendar_date"
    TIME_ZONE_UNCONFIRMED = "time_zone_unconfirmed"
    TIME_ZONE_DATA_UNAVAILABLE = "time_zone_data_unavailable"
    LOCAL_TIME_GAP = "local_time_gap"
    LOCAL_TIME_AMBIGUOUS = "local_time_ambiguous"
    OFFSET_SELECTION_INVALID = "offset_selection_invalid"
    UTC_CONVERSION_OUT_OF_RANGE = "utc_conversion_out_of_range"
    COORDINATES_REQUIRED = "coordinates_required"
    PROVIDER_VERSION_MISMATCH = "provider_version_mismatch"
    TIMELINE_INVALID = "timeline_invalid"


@dataclass(frozen=True, slots=True)
class CalendarTimeError(Exception):
    code: CalendarTimeErrorCode
    field: str
    message: str
