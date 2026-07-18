"""Framework-free value contracts owned by the Calendar & Time context.

These types describe explicit input semantics only. They do not select a calendar
dataset, resolve daylight-saving transitions, convert calendars, or apply Bazi rules.
"""

from dataclasses import dataclass
from decimal import Decimal
from enum import StrEnum


class CalendarType(StrEnum):
    GREGORIAN = "gregorian"
    CHINESE_LUNISOLAR = "chinese_lunisolar"


class DatePrecision(StrEnum):
    YEAR = "year"
    MONTH = "month"
    DAY = "day"


class TimePrecision(StrEnum):
    SECOND = "second"
    MINUTE = "minute"
    HOUR = "hour"
    RANGE = "range"
    UNKNOWN = "unknown"


class TimeZoneResolution(StrEnum):
    RESOLVED = "resolved"
    AMBIGUOUS = "ambiguous"
    UNRESOLVED = "unresolved"


class CoordinatePrecision(StrEnum):
    EXACT = "exact"
    LOCALITY = "locality"
    REGION = "region"
    UNKNOWN = "unknown"


class DataSourceKind(StrEnum):
    USER_PROVIDED = "user_provided"
    CALENDAR_DATASET = "calendar_dataset"
    TIME_ZONE_DATASET = "time_zone_dataset"
    LOCATION_DATASET = "location_dataset"
    EXPERT_GOVERNED = "expert_governed"


class MissingReason(StrEnum):
    NOT_PROVIDED = "not_provided"
    UNKNOWN = "unknown"
    WITHHELD = "withheld"
    NOT_APPLICABLE = "not_applicable"


class UncertaintyCode(StrEnum):
    MISSING = "missing"
    APPROXIMATE = "approximate"
    RANGE_ONLY = "range_only"
    AMBIGUOUS_TIME_ZONE = "ambiguous_time_zone"
    AMBIGUOUS_LOCAL_TIME = "ambiguous_local_time"
    UNVERIFIED_SOURCE = "unverified_source"


@dataclass(frozen=True, slots=True)
class CalendarDate:
    year: int
    month: int | None
    day: int | None
    calendar: CalendarType
    precision: DatePrecision
    leap_month: bool | None = None

    def __post_init__(self) -> None:
        if not 1 <= self.year <= 9999:
            raise ValueError("year must be between 1 and 9999")
        if self.month is not None and not 1 <= self.month <= 12:
            raise ValueError("month must be between 1 and 12")
        if self.day is not None and not 1 <= self.day <= 31:
            raise ValueError("day must be between 1 and 31")
        if self.precision is DatePrecision.DAY and (self.month is None or self.day is None):
            raise ValueError("day precision requires month and day")
        if self.precision is DatePrecision.MONTH and self.month is None:
            raise ValueError("month precision requires month")
        if self.calendar is CalendarType.GREGORIAN and self.leap_month is not None:
            raise ValueError("leap_month applies only to the lunisolar input boundary")


@dataclass(frozen=True, slots=True)
class ClockTime:
    hour: int
    minute: int | None
    second: int | None
    precision: TimePrecision

    def __post_init__(self) -> None:
        if not 0 <= self.hour <= 23:
            raise ValueError("hour must be between 0 and 23")
        if self.minute is not None and not 0 <= self.minute <= 59:
            raise ValueError("minute must be between 0 and 59")
        if self.second is not None and not 0 <= self.second <= 59:
            raise ValueError("second must be between 0 and 59")
        if self.precision is TimePrecision.MINUTE and self.minute is None:
            raise ValueError("minute precision requires minute")
        if self.precision is TimePrecision.SECOND and (self.minute is None or self.second is None):
            raise ValueError("second precision requires minute and second")
        if self.precision in {TimePrecision.RANGE, TimePrecision.UNKNOWN}:
            raise ValueError("range and unknown time require explicit range/missing values")


@dataclass(frozen=True, slots=True)
class TimeRange:
    start: ClockTime
    end: ClockTime

    def __post_init__(self) -> None:
        start = (self.start.hour, self.start.minute or 0, self.start.second or 0)
        end = (self.end.hour, self.end.minute or 0, self.end.second or 0)
        if start > end:
            raise ValueError("time range must be ordered within one local date")
        if (
            self.start.precision is TimePrecision.UNKNOWN
            or self.end.precision is TimePrecision.UNKNOWN
        ):
            raise ValueError("time range boundaries cannot be unknown")


@dataclass(frozen=True, slots=True)
class TimeZoneIdentifier:
    value: str

    def __post_init__(self) -> None:
        value = self.value.strip()
        if not value or len(value) > 255 or any(char.isspace() for char in value):
            raise ValueError("time-zone identifier must be a bounded non-space value")
        object.__setattr__(self, "value", value)


@dataclass(frozen=True, slots=True)
class TimeZoneReference:
    resolution: TimeZoneResolution
    selected: TimeZoneIdentifier | None
    candidates: tuple[TimeZoneIdentifier, ...]
    source_id: str
    source_version: str

    def __post_init__(self) -> None:
        if not self.source_id.strip() or not self.source_version.strip():
            raise ValueError("time-zone source and version are required")
        if self.resolution is TimeZoneResolution.RESOLVED and self.selected is None:
            raise ValueError("resolved time zone requires a selected identifier")
        if self.resolution is not TimeZoneResolution.RESOLVED and self.selected is not None:
            raise ValueError("unresolved time zone cannot silently select an identifier")
        if self.resolution is TimeZoneResolution.AMBIGUOUS and len(self.candidates) < 2:
            raise ValueError("ambiguous time zone requires at least two candidates")


@dataclass(frozen=True, slots=True)
class GeographicCoordinates:
    latitude: Decimal
    longitude: Decimal
    precision: CoordinatePrecision
    source_id: str
    source_version: str

    def __post_init__(self) -> None:
        if not Decimal("-90") <= self.latitude <= Decimal("90"):
            raise ValueError("latitude must be between -90 and 90")
        if not Decimal("-180") <= self.longitude <= Decimal("180"):
            raise ValueError("longitude must be between -180 and 180")
        if not self.source_id.strip() or not self.source_version.strip():
            raise ValueError("coordinate source and version are required")


@dataclass(frozen=True, slots=True)
class DataSourceReference:
    source_id: str
    version: str
    kind: DataSourceKind

    def __post_init__(self) -> None:
        if not self.source_id.strip() or not self.version.strip():
            raise ValueError("data source identity and version are required")


@dataclass(frozen=True, slots=True)
class MissingValue:
    reason: MissingReason


@dataclass(frozen=True, slots=True)
class Uncertainty:
    code: UncertaintyCode
    field: str
    detail: str | None = None

    def __post_init__(self) -> None:
        if not self.field.strip():
            raise ValueError("uncertainty field is required")
