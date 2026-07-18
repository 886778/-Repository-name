from decimal import Decimal

import pytest
from ai_bazi_backend.modules.calendar_time import (
    CalendarDate,
    CalendarType,
    ClockTime,
    CoordinatePrecision,
    DatePrecision,
    GeographicCoordinates,
    TimePrecision,
    TimeRange,
    TimeZoneIdentifier,
    TimeZoneReference,
    TimeZoneResolution,
)


def test_calendar_date_rejects_out_of_range_month() -> None:
    with pytest.raises(ValueError, match="month"):
        CalendarDate(2000, 13, 1, CalendarType.GREGORIAN, DatePrecision.DAY)


def test_gregorian_date_rejects_lunisolar_leap_marker() -> None:
    with pytest.raises(ValueError, match="leap_month"):
        CalendarDate(2000, 1, 1, CalendarType.GREGORIAN, DatePrecision.DAY, True)


def test_ambiguous_time_zone_cannot_silently_select() -> None:
    with pytest.raises(ValueError, match="cannot silently"):
        TimeZoneReference(
            TimeZoneResolution.AMBIGUOUS,
            TimeZoneIdentifier("Zone/Selected"),
            (TimeZoneIdentifier("Zone/A"), TimeZoneIdentifier("Zone/B")),
            "source",
            "1.0.0",
        )


def test_coordinates_are_bounded() -> None:
    with pytest.raises(ValueError, match="latitude"):
        GeographicCoordinates(
            Decimal("90.1"),
            Decimal("0"),
            CoordinatePrecision.LOCALITY,
            "source",
            "1.0.0",
        )


def test_time_range_is_explicit_and_ordered() -> None:
    value = TimeRange(
        ClockTime(8, 0, None, TimePrecision.MINUTE),
        ClockTime(10, 0, None, TimePrecision.MINUTE),
    )
    assert value.start.hour == 8


def test_time_range_rejects_reversed_boundaries() -> None:
    with pytest.raises(ValueError, match="ordered"):
        TimeRange(
            ClockTime(10, 0, None, TimePrecision.MINUTE),
            ClockTime(8, 0, None, TimePrecision.MINUTE),
        )
