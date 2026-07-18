"""Provider interfaces for calendar conversion, time-zone rules, and solar terms."""

from dataclasses import dataclass
from datetime import UTC, date, datetime, timedelta
from enum import StrEnum
from typing import Protocol

from .domain import CalendarDate, CalendarType, DatePrecision, TimeZoneIdentifier
from .errors import CalendarTimeError, CalendarTimeErrorCode
from .sources import CalendarCapability, CalendarDataManifest


@dataclass(frozen=True, slots=True, order=True)
class CivilDate:
    year: int
    month: int
    day: int

    def __post_init__(self) -> None:
        try:
            date(self.year, self.month, self.day)
        except ValueError as error:
            raise ValueError("invalid civil date") from error

    def to_date(self) -> date:
        return date(self.year, self.month, self.day)


@dataclass(frozen=True, slots=True, order=True)
class LocalDateTime:
    date: CivilDate
    hour: int
    minute: int
    second: int

    def __post_init__(self) -> None:
        try:
            datetime(
                self.date.year,
                self.date.month,
                self.date.day,
                self.hour,
                self.minute,
                self.second,
            )
        except ValueError as error:
            raise ValueError("invalid local date-time") from error

    def as_naive_datetime(self) -> datetime:
        return datetime(
            self.date.year,
            self.date.month,
            self.date.day,
            self.hour,
            self.minute,
            self.second,
        )

    @classmethod
    def from_naive_datetime(cls, value: datetime) -> LocalDateTime:
        if value.tzinfo is not None:
            raise ValueError("local date-time must not carry an implicit offset")
        return cls(
            CivilDate(value.year, value.month, value.day),
            value.hour,
            value.minute,
            value.second,
        )


@dataclass(frozen=True, slots=True, order=True)
class UtcOffset:
    seconds: int

    def __post_init__(self) -> None:
        if not -64_800 <= self.seconds <= 64_800:
            raise ValueError("UTC offset must be within plus or minus 18 hours")

    def as_timedelta(self) -> timedelta:
        return timedelta(seconds=self.seconds)


@dataclass(frozen=True, slots=True)
class OffsetCandidate:
    offset: UtcOffset
    daylight_saving: bool | None
    candidate_id: str

    def __post_init__(self) -> None:
        if not self.candidate_id.strip():
            raise ValueError("offset candidate identity cannot be empty")


class OffsetResolutionStatus(StrEnum):
    UNIQUE = "unique"
    AMBIGUOUS = "ambiguous"
    GAP = "gap"
    UNAVAILABLE = "unavailable"


@dataclass(frozen=True, slots=True)
class OffsetResolution:
    status: OffsetResolutionStatus
    candidates: tuple[OffsetCandidate, ...]
    manifest: CalendarDataManifest

    def __post_init__(self) -> None:
        if CalendarCapability.TIME_ZONE_OFFSETS not in self.manifest.capabilities:
            raise ValueError("offset resolution manifest lacks time-zone capability")
        if self.status is OffsetResolutionStatus.UNIQUE and len(self.candidates) != 1:
            raise ValueError("unique offset resolution requires exactly one candidate")
        if self.status is OffsetResolutionStatus.AMBIGUOUS and len(self.candidates) < 2:
            raise ValueError("ambiguous offset resolution requires multiple candidates")
        if (
            self.status in {OffsetResolutionStatus.GAP, OffsetResolutionStatus.UNAVAILABLE}
            and self.candidates
        ):
            raise ValueError("gap or unavailable resolution cannot contain candidates")


@dataclass(frozen=True, slots=True)
class SolarTermIdentifier:
    value: str

    def __post_init__(self) -> None:
        if not self.value.strip():
            raise ValueError("SolarTermIdentifier cannot be empty")


@dataclass(frozen=True, slots=True)
class SolarTermBoundary:
    term_id: SolarTermIdentifier
    instant: datetime
    manifest: CalendarDataManifest

    def __post_init__(self) -> None:
        if self.instant.tzinfo is None or self.instant.utcoffset() != timedelta(0):
            raise ValueError("solar-term boundary must be an aware UTC instant")
        if CalendarCapability.SOLAR_TERM_BOUNDARIES not in self.manifest.capabilities:
            raise ValueError("solar-term manifest lacks boundary capability")


class CalendarProvider(Protocol):
    @property
    def manifest(self) -> CalendarDataManifest: ...

    def supports(self, calendar: CalendarType) -> bool: ...

    def to_civil_date(self, value: CalendarDate) -> CivilDate: ...


class TimeZoneRulesProvider(Protocol):
    @property
    def manifest(self) -> CalendarDataManifest: ...

    def resolve_offset(
        self, zone: TimeZoneIdentifier, local_time: LocalDateTime
    ) -> OffsetResolution: ...


class SolarTermProvider(Protocol):
    @property
    def manifest(self) -> CalendarDataManifest: ...

    def boundaries_between(
        self,
        start: datetime,
        end: datetime,
    ) -> tuple[SolarTermBoundary, ...]: ...


@dataclass(frozen=True, slots=True)
class ProlepticGregorianProvider:
    """Data-free civil validation only; it performs no lunisolar conversion."""

    manifest: CalendarDataManifest

    def __post_init__(self) -> None:
        if CalendarCapability.GREGORIAN_VALIDATION not in self.manifest.capabilities:
            raise ValueError("Gregorian provider manifest lacks validation capability")

    def supports(self, calendar: CalendarType) -> bool:
        return calendar is CalendarType.GREGORIAN

    def to_civil_date(self, value: CalendarDate) -> CivilDate:
        if not self.supports(value.calendar):
            raise CalendarTimeError(
                CalendarTimeErrorCode.UNSUPPORTED_CALENDAR,
                "birth_date.calendar",
                "calendar conversion requires an explicitly approved provider",
            )
        if value.precision is not DatePrecision.DAY or value.month is None or value.day is None:
            raise CalendarTimeError(
                CalendarTimeErrorCode.DATE_PRECISION_INSUFFICIENT,
                "birth_date.precision",
                "day precision is required for instant normalization",
            )
        try:
            return CivilDate(value.year, value.month, value.day)
        except ValueError as error:
            raise CalendarTimeError(
                CalendarTimeErrorCode.INVALID_CALENDAR_DATE,
                "birth_date",
                "calendar date is invalid",
            ) from error


def local_to_utc(local_time: LocalDateTime, offset: UtcOffset) -> datetime:
    """Convert using an explicit offset; never consult host time-zone state."""

    try:
        naive_utc = local_time.as_naive_datetime() - offset.as_timedelta()
    except OverflowError as error:
        raise CalendarTimeError(
            CalendarTimeErrorCode.UTC_CONVERSION_OUT_OF_RANGE,
            "birth_time",
            "UTC conversion exceeds the supported civil date range",
        ) from error
    return naive_utc.replace(tzinfo=UTC)
