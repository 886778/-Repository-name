"""Framework-independent Birth context types."""

from dataclasses import dataclass
from enum import StrEnum

from ai_bazi_backend.modules.calendar_time import (
    CalendarDate,
    ClockTime,
    DataSourceReference,
    GeographicCoordinates,
    MissingValue,
    TimeRange,
    TimeZoneReference,
    Uncertainty,
)


@dataclass(frozen=True, slots=True)
class BirthInputId:
    value: str

    def __post_init__(self) -> None:
        if not self.value.strip():
            raise ValueError("BirthInputId cannot be empty")


@dataclass(frozen=True, slots=True)
class RawText:
    value: str


class RuleSexMarker(StrEnum):
    MALE = "male"
    FEMALE = "female"
    UNSPECIFIED = "unspecified"


class ConfirmationStatus(StrEnum):
    UNCONFIRMED = "unconfirmed"
    CONFIRMED = "confirmed"
    REJECTED = "rejected"


@dataclass(frozen=True, slots=True)
class RawBirthInput:
    schema_version: str
    input_id: BirthInputId
    calendar_text: RawText
    date_text: RawText
    time_text: RawText | MissingValue
    place_text: RawText | MissingValue
    time_zone_text: RawText | MissingValue
    rule_sex_marker: RuleSexMarker
    source: DataSourceReference
    confirmation: ConfirmationStatus

    def __post_init__(self) -> None:
        if not self.schema_version.strip():
            raise ValueError("schema version is required")


@dataclass(frozen=True, slots=True)
class ValidatedBirthInput:
    schema_version: str
    input_id: BirthInputId
    birth_date: CalendarDate
    birth_time: ClockTime | TimeRange | MissingValue
    time_zone: TimeZoneReference
    coordinates: GeographicCoordinates | MissingValue
    rule_sex_marker: RuleSexMarker
    source: DataSourceReference
    confirmation: ConfirmationStatus
    uncertainties: tuple[Uncertainty, ...] = ()


@dataclass(frozen=True, slots=True)
class CanonicalBirthInput:
    schema_version: str
    input_id: BirthInputId
    birth_date: CalendarDate
    birth_time: ClockTime | TimeRange | MissingValue
    time_zone: TimeZoneReference
    coordinates: GeographicCoordinates | MissingValue
    rule_sex_marker: RuleSexMarker
    source_chain: tuple[DataSourceReference, ...]
    uncertainties: tuple[Uncertainty, ...]
    confirmation: ConfirmationStatus

    def __post_init__(self) -> None:
        if self.confirmation is not ConfirmationStatus.CONFIRMED:
            raise ValueError("canonical input must be explicitly confirmed")
        if not self.source_chain:
            raise ValueError("canonical input requires a source chain")
