"""Deterministic calendar and time normalization engine."""

from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import StrEnum

from .domain import (
    CalendarDate,
    ClockTime,
    DataSourceReference,
    GeographicCoordinates,
    MissingValue,
    TimeRange,
    TimeZoneIdentifier,
    TimeZoneReference,
)
from .errors import CalendarTimeError, CalendarTimeErrorCode
from .providers import (
    CalendarProvider,
    CivilDate,
    LocalDateTime,
    OffsetCandidate,
    OffsetResolution,
    OffsetResolutionStatus,
    TimeZoneRulesProvider,
    local_to_utc,
)
from .strategies import DayBoundaryStrategy, TrueSolarTimeStrategy
from .timeline import (
    NormalizedInstant,
    TimeComputationStep,
    TimeComputationTimeline,
    TimeDerivationId,
    TimeTimelineNode,
)
from .validation import CalendarValidator, require_confirmed_time_zone


class TimeNormalizationStatus(StrEnum):
    EXACT = "exact"
    RANGE = "range"
    INDETERMINATE = "indeterminate"


@dataclass(frozen=True, slots=True)
class OffsetSelection:
    candidate_id: str

    def __post_init__(self) -> None:
        if not self.candidate_id.strip():
            raise ValueError("offset selection cannot be empty")


@dataclass(frozen=True, slots=True)
class TimeNormalizationInput:
    input_reference_id: str
    birth_date: CalendarDate
    birth_time: ClockTime | TimeRange | MissingValue
    time_zone: TimeZoneReference
    coordinates: GeographicCoordinates | MissingValue
    source_chain: tuple[DataSourceReference, ...]

    def __post_init__(self) -> None:
        if not self.input_reference_id.strip() or not self.source_chain:
            raise ValueError("normalization input identity and source chain are required")


@dataclass(frozen=True, slots=True)
class NormalizedTimePoint:
    civil_local_time: LocalDateTime
    adjusted_local_time: LocalDateTime
    instant: NormalizedInstant
    logical_date: CivilDate
    offset_candidate_id: str


@dataclass(frozen=True, slots=True)
class TimeNormalizationRequest:
    request_id: str
    time_input: TimeNormalizationInput
    performed_at: datetime
    offset_selection: OffsetSelection | None = None

    def __post_init__(self) -> None:
        if not self.request_id.strip():
            raise ValueError("normalization request identity cannot be empty")
        if self.performed_at.tzinfo is None or self.performed_at.utcoffset() != timedelta(0):
            raise ValueError("normalization performed_at must be an aware UTC instant")


@dataclass(frozen=True, slots=True)
class TimeNormalizationResult:
    status: TimeNormalizationStatus
    points: tuple[NormalizedTimePoint, ...]
    timeline: TimeComputationTimeline
    performed_at: datetime
    provider_manifest_ids: tuple[str, ...]

    def __post_init__(self) -> None:
        expected = {
            TimeNormalizationStatus.EXACT: 1,
            TimeNormalizationStatus.RANGE: 2,
            TimeNormalizationStatus.INDETERMINATE: 0,
        }[self.status]
        if len(self.points) != expected:
            raise ValueError("normalization status and point count are inconsistent")
        if not self.provider_manifest_ids:
            raise ValueError("normalization result requires provider manifests")


@dataclass(frozen=True, slots=True)
class TimeNormalizationEngine:
    calendar_provider: CalendarProvider
    time_zone_provider: TimeZoneRulesProvider
    day_boundary_strategy: DayBoundaryStrategy
    true_solar_time_strategy: TrueSolarTimeStrategy

    def normalize(self, request: TimeNormalizationRequest) -> TimeNormalizationResult:
        time_input = request.time_input
        validation = CalendarValidator().validate(
            time_input.birth_date,
            self.calendar_provider,
        )
        nodes = self._base_timeline(request, validation.civil_date)
        manifests = self._manifest_ids()

        if isinstance(time_input.birth_time, MissingValue):
            return TimeNormalizationResult(
                TimeNormalizationStatus.INDETERMINATE,
                (),
                TimeComputationTimeline("1.0.0", tuple(nodes)),
                request.performed_at,
                manifests,
            )

        require_confirmed_time_zone(time_input.time_zone)
        zone = time_input.time_zone.selected
        assert zone is not None
        self._validate_time_zone_manifest(request)

        clocks: tuple[ClockTime, ...]
        if isinstance(time_input.birth_time, TimeRange):
            clocks = (time_input.birth_time.start, time_input.birth_time.end)
            status = TimeNormalizationStatus.RANGE
        else:
            clocks = (time_input.birth_time,)
            status = TimeNormalizationStatus.EXACT

        points: list[NormalizedTimePoint] = []
        parent = nodes[-1].derivation_id
        for index, clock in enumerate(clocks):
            point, point_nodes = self._normalize_point(
                request,
                validation.civil_date,
                clock,
                zone,
                index,
                parent,
            )
            points.append(point)
            nodes.extend(point_nodes)
            parent = point_nodes[-1].derivation_id

        return TimeNormalizationResult(
            status,
            tuple(points),
            TimeComputationTimeline("1.0.0", tuple(nodes)),
            request.performed_at,
            manifests,
        )

    def _normalize_point(
        self,
        request: TimeNormalizationRequest,
        civil_date: CivilDate,
        clock: ClockTime,
        zone: TimeZoneIdentifier,
        index: int,
        parent: TimeDerivationId,
    ) -> tuple[NormalizedTimePoint, tuple[TimeTimelineNode, ...]]:
        local = LocalDateTime(
            civil_date,
            clock.hour,
            clock.minute or 0,
            clock.second or 0,
        )
        resolution = self.time_zone_provider.resolve_offset(zone, local)
        if resolution.manifest != self.time_zone_provider.manifest:
            raise CalendarTimeError(
                CalendarTimeErrorCode.PROVIDER_VERSION_MISMATCH,
                "time_zone.resolution",
                "offset resolution manifest differs from the provider manifest",
            )
        candidate = self._select_offset(resolution, request.offset_selection)
        utc_instant = local_to_utc(local, candidate.offset)
        adjustment = self.true_solar_time_strategy.adjust(local, request.time_input.coordinates)
        boundary = self.day_boundary_strategy.resolve(adjustment.adjusted_local_time)
        prefix = f"{request.request_id}:point:{index}"
        timezone_id = TimeDerivationId(f"{prefix}:timezone")
        utc_id = TimeDerivationId(f"{prefix}:utc")
        solar_id = TimeDerivationId(f"{prefix}:solar")
        boundary_id = TimeDerivationId(f"{prefix}:boundary")
        nodes = (
            TimeTimelineNode(
                2 + index * 4,
                timezone_id,
                TimeComputationStep.TIME_ZONE_RESOLVED,
                f"{zone.value}:{candidate.offset.seconds}:{candidate.candidate_id}",
                (parent,),
                resolution.manifest.source_id.value,
                resolution.manifest.version.value,
            ),
            TimeTimelineNode(
                3 + index * 4,
                utc_id,
                TimeComputationStep.UTC_CONVERTED,
                utc_instant.isoformat(),
                (timezone_id,),
                resolution.manifest.source_id.value,
                resolution.manifest.version.value,
            ),
            TimeTimelineNode(
                4 + index * 4,
                solar_id,
                TimeComputationStep.TRUE_SOLAR_TIME_APPLIED,
                f"applied={adjustment.applied};delta={adjustment.delta_seconds}",
                (utc_id,),
                adjustment.manifest.source_id.value,
                adjustment.manifest.version.value,
            ),
            TimeTimelineNode(
                5 + index * 4,
                boundary_id,
                TimeComputationStep.DAY_BOUNDARY_RESOLVED,
                boundary.logical_date.to_date().isoformat(),
                (solar_id,),
                boundary.manifest.source_id.value,
                boundary.manifest.version.value,
            ),
        )
        point = NormalizedTimePoint(
            local,
            adjustment.adjusted_local_time,
            NormalizedInstant(
                utc_instant,
                local.as_naive_datetime().isoformat(),
                candidate.offset.seconds,
            ),
            boundary.logical_date,
            candidate.candidate_id,
        )
        return point, nodes

    def _base_timeline(
        self,
        request: TimeNormalizationRequest,
        civil_date: CivilDate,
    ) -> list[TimeTimelineNode]:
        input_id = TimeDerivationId(f"{request.request_id}:input")
        calendar_id = TimeDerivationId(f"{request.request_id}:calendar")
        source = request.time_input.source_chain[0]
        return [
            TimeTimelineNode(
                0,
                input_id,
                TimeComputationStep.INPUT_ACCEPTED,
                request.time_input.input_reference_id,
                (),
                source.source_id,
                source.version,
            ),
            TimeTimelineNode(
                1,
                calendar_id,
                TimeComputationStep.CALENDAR_VALIDATED,
                civil_date.to_date().isoformat(),
                (input_id,),
                self.calendar_provider.manifest.source_id.value,
                self.calendar_provider.manifest.version.value,
            ),
        ]

    def _validate_time_zone_manifest(self, request: TimeNormalizationRequest) -> None:
        reference = request.time_input.time_zone
        manifest = self.time_zone_provider.manifest
        if (
            reference.source_id != manifest.source_id.value
            or reference.source_version != manifest.version.value
        ):
            raise CalendarTimeError(
                CalendarTimeErrorCode.PROVIDER_VERSION_MISMATCH,
                "time_zone.source",
                "time-zone reference and provider manifest do not match",
            )

    @staticmethod
    def _select_offset(
        resolution: OffsetResolution,
        selection: OffsetSelection | None,
    ) -> OffsetCandidate:
        if resolution.status is OffsetResolutionStatus.GAP:
            raise CalendarTimeError(
                CalendarTimeErrorCode.LOCAL_TIME_GAP,
                "birth_time",
                "local time does not exist under the selected time-zone rules",
            )
        if resolution.status is OffsetResolutionStatus.UNAVAILABLE:
            raise CalendarTimeError(
                CalendarTimeErrorCode.TIME_ZONE_DATA_UNAVAILABLE,
                "time_zone",
                "time-zone data is unavailable for this local time",
            )
        if resolution.status is OffsetResolutionStatus.UNIQUE:
            return resolution.candidates[0]
        if selection is None:
            raise CalendarTimeError(
                CalendarTimeErrorCode.LOCAL_TIME_AMBIGUOUS,
                "birth_time",
                "ambiguous local time requires an explicit offset selection",
            )
        matches = tuple(
            candidate
            for candidate in resolution.candidates
            if candidate.candidate_id == selection.candidate_id
        )
        if len(matches) != 1:
            raise CalendarTimeError(
                CalendarTimeErrorCode.OFFSET_SELECTION_INVALID,
                "offset_selection",
                "selected offset candidate is not part of the provider result",
            )
        return matches[0]

    def _manifest_ids(self) -> tuple[str, ...]:
        manifests = (
            self.calendar_provider.manifest,
            self.time_zone_provider.manifest,
            self.day_boundary_strategy.manifest,
            self.true_solar_time_strategy.manifest,
        )
        identifiers = tuple(
            f"{item.source_id.value}@{item.version.value}#{item.checksum}" for item in manifests
        )
        return tuple(dict.fromkeys(identifiers))
