"""Calendar/time validation independent from provider implementation details."""

from dataclasses import dataclass

from .domain import CalendarDate, CalendarType, TimeZoneReference, TimeZoneResolution
from .errors import CalendarTimeError, CalendarTimeErrorCode
from .providers import CalendarProvider, CivilDate


@dataclass(frozen=True, slots=True)
class CalendarValidationResult:
    civil_date: CivilDate
    calendar: CalendarType
    provider_source_id: str
    provider_version: str


class CalendarValidator:
    def validate(
        self,
        value: CalendarDate,
        provider: CalendarProvider,
    ) -> CalendarValidationResult:
        if not provider.supports(value.calendar):
            raise CalendarTimeError(
                CalendarTimeErrorCode.UNSUPPORTED_CALENDAR,
                "birth_date.calendar",
                "selected calendar provider does not support this calendar",
            )
        civil_date = provider.to_civil_date(value)
        return CalendarValidationResult(
            civil_date,
            value.calendar,
            provider.manifest.source_id.value,
            provider.manifest.version.value,
        )


def require_confirmed_time_zone(value: TimeZoneReference) -> None:
    if value.resolution is not TimeZoneResolution.RESOLVED or value.selected is None:
        raise CalendarTimeError(
            CalendarTimeErrorCode.TIME_ZONE_UNCONFIRMED,
            "time_zone",
            "time zone must be explicitly resolved before normalization",
        )
