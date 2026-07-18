"""Versioned source manifests for calendar and time providers."""

from dataclasses import dataclass
from enum import StrEnum


class CalendarCapability(StrEnum):
    GREGORIAN_VALIDATION = "gregorian_validation"
    CALENDAR_CONVERSION = "calendar_conversion"
    TIME_ZONE_OFFSETS = "time_zone_offsets"
    SOLAR_TERM_BOUNDARIES = "solar_term_boundaries"
    TRUE_SOLAR_TIME = "true_solar_time"
    DAY_BOUNDARY = "day_boundary"


@dataclass(frozen=True, slots=True)
class CalendarDataSourceId:
    value: str

    def __post_init__(self) -> None:
        if not self.value.strip():
            raise ValueError("CalendarDataSourceId cannot be empty")


@dataclass(frozen=True, slots=True)
class CalendarDataVersion:
    value: str

    def __post_init__(self) -> None:
        if not self.value.strip():
            raise ValueError("CalendarDataVersion cannot be empty")


@dataclass(frozen=True, slots=True)
class CalendarDataManifest:
    source_id: CalendarDataSourceId
    version: CalendarDataVersion
    checksum: str
    capabilities: tuple[CalendarCapability, ...]

    def __post_init__(self) -> None:
        if not self.checksum.strip():
            raise ValueError("calendar data checksum cannot be empty")
        if not self.capabilities:
            raise ValueError("calendar data manifest requires capabilities")
        if len(self.capabilities) != len(set(self.capabilities)):
            raise ValueError("calendar data capabilities must be unique")
