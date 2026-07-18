from dataclasses import dataclass, replace
from datetime import UTC, datetime, timedelta
from decimal import Decimal

import pytest
from ai_bazi_backend.modules.calendar_time import (
    CalendarCapability,
    CalendarDataManifest,
    CalendarDataSourceId,
    CalendarDataVersion,
    CalendarDate,
    CalendarTimeError,
    CalendarTimeErrorCode,
    CalendarType,
    CivilDate,
    CivilMidnightBoundaryStrategy,
    ClockTime,
    CoordinatePrecision,
    DataSourceKind,
    DataSourceReference,
    DatePrecision,
    DisabledTrueSolarTimeStrategy,
    GeographicCoordinates,
    LocalDateTime,
    MissingReason,
    MissingValue,
    OffsetCandidate,
    OffsetResolution,
    OffsetResolutionStatus,
    OffsetSelection,
    ProlepticGregorianProvider,
    SolarTermBoundary,
    SolarTermIdentifier,
    TimeComputationStep,
    TimeComputationTimeline,
    TimeDerivationId,
    TimeNormalizationEngine,
    TimeNormalizationInput,
    TimeNormalizationRequest,
    TimeNormalizationStatus,
    TimePrecision,
    TimeRange,
    TimeTimelineNode,
    TimeZoneIdentifier,
    TimeZoneReference,
    TimeZoneResolution,
    TrueSolarTimeAdjustment,
    UtcOffset,
    local_to_utc,
    time_normalization_result_to_document,
)
from hypothesis import given
from hypothesis import strategies as st


def manifest(name: str, capability: CalendarCapability) -> CalendarDataManifest:
    return CalendarDataManifest(
        CalendarDataSourceId(name),
        CalendarDataVersion("1.0.0"),
        f"checksum-{name}",
        (capability,),
    )


@dataclass(frozen=True, slots=True)
class StubTimeZoneProvider:
    manifest: CalendarDataManifest
    resolution: OffsetResolution

    def resolve_offset(
        self,
        zone: TimeZoneIdentifier,
        local_time: LocalDateTime,
    ) -> OffsetResolution:
        del zone, local_time
        return self.resolution


@dataclass(frozen=True, slots=True)
class ShiftSolarTimeStrategy:
    manifest: CalendarDataManifest
    delta_seconds: int
    strategy_id: str = "test-only-shift"
    strategy_version: str = "0.0.0"

    def adjust(
        self,
        local_time: LocalDateTime,
        coordinates: GeographicCoordinates | MissingValue,
    ) -> TrueSolarTimeAdjustment:
        del coordinates
        shifted = local_time.as_naive_datetime() + timedelta(seconds=self.delta_seconds)
        return TrueSolarTimeAdjustment(
            LocalDateTime.from_naive_datetime(shifted),
            self.delta_seconds,
            True,
            self.strategy_id,
            self.strategy_version,
            self.manifest,
        )


@dataclass(frozen=True, slots=True)
class StubSolarTermProvider:
    manifest: CalendarDataManifest
    boundaries: tuple[SolarTermBoundary, ...]

    def boundaries_between(
        self,
        start: datetime,
        end: datetime,
    ) -> tuple[SolarTermBoundary, ...]:
        return tuple(item for item in self.boundaries if start <= item.instant < end)


def normalization_input(
    birth_time: ClockTime | TimeRange | MissingValue | None = None,
    calendar: CalendarType = CalendarType.GREGORIAN,
) -> TimeNormalizationInput:
    source = DataSourceReference("fixture", "1.0.0", DataSourceKind.USER_PROVIDED)
    return TimeNormalizationInput(
        input_reference_id="birth-input-calendar-engine",
        birth_date=CalendarDate(2000, 1, 2, calendar, DatePrecision.DAY),
        birth_time=birth_time or ClockTime(3, 4, 5, TimePrecision.SECOND),
        time_zone=TimeZoneReference(
            TimeZoneResolution.RESOLVED,
            TimeZoneIdentifier("Test/Zone"),
            (),
            "test-time-zone",
            "1.0.0",
        ),
        coordinates=GeographicCoordinates(
            Decimal("39.9"),
            Decimal("116.4"),
            CoordinatePrecision.LOCALITY,
            "test-location",
            "1.0.0",
        ),
        source_chain=(source,),
    )


def engine(resolution: OffsetResolution) -> TimeNormalizationEngine:
    return TimeNormalizationEngine(
        ProlepticGregorianProvider(manifest("gregorian", CalendarCapability.GREGORIAN_VALIDATION)),
        StubTimeZoneProvider(resolution.manifest, resolution),
        CivilMidnightBoundaryStrategy(manifest("civil-day", CalendarCapability.DAY_BOUNDARY)),
        DisabledTrueSolarTimeStrategy(
            manifest("solar-disabled", CalendarCapability.TRUE_SOLAR_TIME)
        ),
    )


def unique_resolution(offset_seconds: int = 28_800) -> OffsetResolution:
    source = manifest("test-time-zone", CalendarCapability.TIME_ZONE_OFFSETS)
    return OffsetResolution(
        OffsetResolutionStatus.UNIQUE,
        (OffsetCandidate(UtcOffset(offset_seconds), False, "offset-1"),),
        source,
    )


def request(time_input: TimeNormalizationInput | None = None) -> TimeNormalizationRequest:
    return TimeNormalizationRequest(
        "normalization-1",
        time_input or normalization_input(),
        datetime(2026, 1, 1, tzinfo=UTC),
    )


def test_exact_time_normalization_is_traceable() -> None:
    result = engine(unique_resolution()).normalize(request())
    assert result.status is TimeNormalizationStatus.EXACT
    assert result.points[0].instant.utc_instant == datetime(2000, 1, 1, 19, 4, 5, tzinfo=UTC)
    assert tuple(node.step for node in result.timeline.nodes) == (
        TimeComputationStep.INPUT_ACCEPTED,
        TimeComputationStep.CALENDAR_VALIDATED,
        TimeComputationStep.TIME_ZONE_RESOLVED,
        TimeComputationStep.UTC_CONVERTED,
        TimeComputationStep.TRUE_SOLAR_TIME_APPLIED,
        TimeComputationStep.DAY_BOUNDARY_RESOLVED,
    )


def test_same_request_and_versions_produce_equal_result() -> None:
    calendar_engine = engine(unique_resolution())
    assert calendar_engine.normalize(request()) == calendar_engine.normalize(request())


def test_normalization_result_has_stable_document_mapping() -> None:
    document = time_normalization_result_to_document(
        engine(unique_resolution()).normalize(request())
    )
    assert document["schemaVersion"] == "1.0.0"
    assert document["points"][0]["utcInstant"] == "2000-01-01T19:04:05+00:00"
    assert len(document["timeline"]) == 6


def test_unknown_time_remains_indeterminate() -> None:
    result = engine(unique_resolution()).normalize(
        request(normalization_input(MissingValue(MissingReason.UNKNOWN)))
    )
    assert result.status is TimeNormalizationStatus.INDETERMINATE
    assert result.points == ()


def test_time_range_produces_two_ordered_points() -> None:
    time_range = TimeRange(
        ClockTime(8, 0, None, TimePrecision.MINUTE),
        ClockTime(10, 0, None, TimePrecision.MINUTE),
    )
    result = engine(unique_resolution()).normalize(request(normalization_input(time_range)))
    assert result.status is TimeNormalizationStatus.RANGE
    assert result.points[0].instant.utc_instant < result.points[1].instant.utc_instant
    assert len(result.timeline.nodes) == 10


def test_gap_is_explicit_failure() -> None:
    source = manifest("test-time-zone", CalendarCapability.TIME_ZONE_OFFSETS)
    resolution = OffsetResolution(OffsetResolutionStatus.GAP, (), source)
    with pytest.raises(CalendarTimeError) as captured:
        engine(resolution).normalize(request())
    assert captured.value.code is CalendarTimeErrorCode.LOCAL_TIME_GAP


def test_unavailable_time_zone_data_is_explicit_failure() -> None:
    source = manifest("test-time-zone", CalendarCapability.TIME_ZONE_OFFSETS)
    resolution = OffsetResolution(OffsetResolutionStatus.UNAVAILABLE, (), source)
    with pytest.raises(CalendarTimeError) as captured:
        engine(resolution).normalize(request())
    assert captured.value.code is CalendarTimeErrorCode.TIME_ZONE_DATA_UNAVAILABLE


def test_ambiguous_time_requires_explicit_candidate() -> None:
    source = manifest("test-time-zone", CalendarCapability.TIME_ZONE_OFFSETS)
    resolution = OffsetResolution(
        OffsetResolutionStatus.AMBIGUOUS,
        (
            OffsetCandidate(UtcOffset(3_600), True, "summer"),
            OffsetCandidate(UtcOffset(0), False, "standard"),
        ),
        source,
    )
    with pytest.raises(CalendarTimeError) as captured:
        engine(resolution).normalize(request())
    assert captured.value.code is CalendarTimeErrorCode.LOCAL_TIME_AMBIGUOUS


def test_ambiguous_time_accepts_only_provider_candidate() -> None:
    source = manifest("test-time-zone", CalendarCapability.TIME_ZONE_OFFSETS)
    resolution = OffsetResolution(
        OffsetResolutionStatus.AMBIGUOUS,
        (
            OffsetCandidate(UtcOffset(3_600), True, "summer"),
            OffsetCandidate(UtcOffset(0), False, "standard"),
        ),
        source,
    )
    selected = replace(request(), offset_selection=OffsetSelection("standard"))
    result = engine(resolution).normalize(selected)
    assert result.points[0].offset_candidate_id == "standard"
    with pytest.raises(CalendarTimeError) as captured:
        engine(resolution).normalize(replace(request(), offset_selection=OffsetSelection("other")))
    assert captured.value.code is CalendarTimeErrorCode.OFFSET_SELECTION_INVALID


def test_provider_version_mismatch_is_rejected() -> None:
    snapshot = replace(
        normalization_input(),
        time_zone=TimeZoneReference(
            TimeZoneResolution.RESOLVED,
            TimeZoneIdentifier("Test/Zone"),
            (),
            "different-source",
            "1.0.0",
        ),
    )
    with pytest.raises(CalendarTimeError) as captured:
        engine(unique_resolution()).normalize(request(snapshot))
    assert captured.value.code is CalendarTimeErrorCode.PROVIDER_VERSION_MISMATCH


def test_unconfirmed_time_zone_is_rejected() -> None:
    snapshot = replace(
        normalization_input(),
        time_zone=TimeZoneReference(
            TimeZoneResolution.AMBIGUOUS,
            None,
            (TimeZoneIdentifier("Test/A"), TimeZoneIdentifier("Test/B")),
            "test-time-zone",
            "1.0.0",
        ),
    )
    with pytest.raises(CalendarTimeError) as captured:
        engine(unique_resolution()).normalize(request(snapshot))
    assert captured.value.code is CalendarTimeErrorCode.TIME_ZONE_UNCONFIRMED


def test_resolution_manifest_must_match_provider() -> None:
    provider_manifest = manifest("test-time-zone", CalendarCapability.TIME_ZONE_OFFSETS)
    result_manifest = manifest("other-time-zone", CalendarCapability.TIME_ZONE_OFFSETS)
    resolution = OffsetResolution(
        OffsetResolutionStatus.UNIQUE,
        (OffsetCandidate(UtcOffset(0), False, "offset-1"),),
        result_manifest,
    )
    calendar_engine = TimeNormalizationEngine(
        ProlepticGregorianProvider(manifest("gregorian", CalendarCapability.GREGORIAN_VALIDATION)),
        StubTimeZoneProvider(provider_manifest, resolution),
        CivilMidnightBoundaryStrategy(manifest("civil-day", CalendarCapability.DAY_BOUNDARY)),
        DisabledTrueSolarTimeStrategy(
            manifest("solar-disabled", CalendarCapability.TRUE_SOLAR_TIME)
        ),
    )
    with pytest.raises(CalendarTimeError) as captured:
        calendar_engine.normalize(request())
    assert captured.value.code is CalendarTimeErrorCode.PROVIDER_VERSION_MISMATCH


def test_lunisolar_conversion_remains_provider_gated() -> None:
    with pytest.raises(CalendarTimeError) as captured:
        engine(unique_resolution()).normalize(
            request(normalization_input(calendar=CalendarType.CHINESE_LUNISOLAR))
        )
    assert captured.value.code is CalendarTimeErrorCode.UNSUPPORTED_CALENDAR


def test_invalid_gregorian_date_is_rejected() -> None:
    snapshot = replace(
        normalization_input(),
        birth_date=CalendarDate(2001, 2, 29, CalendarType.GREGORIAN, DatePrecision.DAY),
    )
    with pytest.raises(CalendarTimeError) as captured:
        engine(unique_resolution()).normalize(request(snapshot))
    assert captured.value.code is CalendarTimeErrorCode.INVALID_CALENDAR_DATE


def test_day_precision_is_required_for_instant_normalization() -> None:
    snapshot = replace(
        normalization_input(),
        birth_date=CalendarDate(2001, 2, None, CalendarType.GREGORIAN, DatePrecision.MONTH),
    )
    with pytest.raises(CalendarTimeError) as captured:
        engine(unique_resolution()).normalize(request(snapshot))
    assert captured.value.code is CalendarTimeErrorCode.DATE_PRECISION_INSUFFICIENT


def test_civil_boundary_is_not_zi_hour_rule() -> None:
    strategy = CivilMidnightBoundaryStrategy(manifest("civil-day", CalendarCapability.DAY_BOUNDARY))
    local = LocalDateTime(CivilDate(2000, 1, 2), 23, 30, 0)
    assert strategy.resolve(local).logical_date == CivilDate(2000, 1, 2)
    assert strategy.strategy_id == "civil-midnight"


def test_true_solar_extension_can_be_injected_without_formula_in_production() -> None:
    source = unique_resolution()
    calendar_engine = TimeNormalizationEngine(
        ProlepticGregorianProvider(manifest("gregorian", CalendarCapability.GREGORIAN_VALIDATION)),
        StubTimeZoneProvider(source.manifest, source),
        CivilMidnightBoundaryStrategy(manifest("civil-day", CalendarCapability.DAY_BOUNDARY)),
        ShiftSolarTimeStrategy(
            manifest("test-solar", CalendarCapability.TRUE_SOLAR_TIME),
            3_600,
        ),
    )
    result = calendar_engine.normalize(request())
    assert result.points[0].adjusted_local_time.hour == 4
    assert result.points[0].instant.utc_instant.hour == 19


def test_solar_term_provider_contract_returns_only_requested_range() -> None:
    source = manifest("solar-terms-pending", CalendarCapability.SOLAR_TERM_BOUNDARIES)
    boundary = SolarTermBoundary(
        SolarTermIdentifier("example-only"),
        datetime(2026, 2, 1, tzinfo=UTC),
        source,
    )
    provider = StubSolarTermProvider(source, (boundary,))
    assert provider.boundaries_between(
        datetime(2026, 1, 1, tzinfo=UTC),
        datetime(2026, 3, 1, tzinfo=UTC),
    ) == (boundary,)


def test_timeline_rejects_non_contiguous_sequence() -> None:
    with pytest.raises(CalendarTimeError) as captured:
        TimeComputationTimeline(
            "1.0.0",
            (
                TimeTimelineNode(
                    1,
                    TimeDerivationId("node-1"),
                    TimeComputationStep.INPUT_ACCEPTED,
                    "value",
                    (),
                    "source",
                    "1.0.0",
                ),
            ),
        )
    assert captured.value.code is CalendarTimeErrorCode.TIMELINE_INVALID


def test_utc_conversion_out_of_supported_range_is_typed() -> None:
    value = LocalDateTime(CivilDate(1, 1, 1), 0, 0, 0)
    with pytest.raises(CalendarTimeError) as captured:
        local_to_utc(value, UtcOffset(64_800))
    assert captured.value.code is CalendarTimeErrorCode.UTC_CONVERSION_OUT_OF_RANGE


@given(
    st.datetimes(
        min_value=datetime(1900, 1, 1),
        max_value=datetime(2100, 12, 31, 23, 59, 59),
        timezones=st.none(),
    ).map(lambda value: value.replace(microsecond=0)),
    st.integers(min_value=-64_800, max_value=64_800),
)
def test_explicit_offset_conversion_is_deterministic(local: datetime, offset: int) -> None:
    value = LocalDateTime.from_naive_datetime(local)
    expected = (local - timedelta(seconds=offset)).replace(tzinfo=UTC)
    assert local_to_utc(value, UtcOffset(offset)) == expected
