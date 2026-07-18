"""Explicit day-boundary and true-solar-time extension contracts."""

from dataclasses import dataclass
from datetime import timedelta
from typing import Protocol

from .domain import GeographicCoordinates, MissingValue
from .providers import CivilDate, LocalDateTime
from .sources import CalendarCapability, CalendarDataManifest


@dataclass(frozen=True, slots=True)
class DayBoundaryResult:
    logical_date: CivilDate
    strategy_id: str
    strategy_version: str
    manifest: CalendarDataManifest


class DayBoundaryStrategy(Protocol):
    @property
    def strategy_id(self) -> str: ...

    @property
    def strategy_version(self) -> str: ...

    @property
    def manifest(self) -> CalendarDataManifest: ...

    def resolve(self, local_time: LocalDateTime) -> DayBoundaryResult: ...


@dataclass(frozen=True, slots=True)
class CivilMidnightBoundaryStrategy:
    """Neutral civil-date boundary; not a Bazi zi-hour decision."""

    manifest: CalendarDataManifest
    strategy_id: str = "civil-midnight"
    strategy_version: str = "1.0.0"

    def __post_init__(self) -> None:
        if CalendarCapability.DAY_BOUNDARY not in self.manifest.capabilities:
            raise ValueError("day-boundary manifest lacks required capability")

    def resolve(self, local_time: LocalDateTime) -> DayBoundaryResult:
        return DayBoundaryResult(
            local_time.date,
            self.strategy_id,
            self.strategy_version,
            self.manifest,
        )


@dataclass(frozen=True, slots=True)
class TrueSolarTimeAdjustment:
    adjusted_local_time: LocalDateTime
    delta_seconds: int
    applied: bool
    strategy_id: str
    strategy_version: str
    manifest: CalendarDataManifest


class TrueSolarTimeStrategy(Protocol):
    @property
    def strategy_id(self) -> str: ...

    @property
    def strategy_version(self) -> str: ...

    @property
    def manifest(self) -> CalendarDataManifest: ...

    def adjust(
        self,
        local_time: LocalDateTime,
        coordinates: GeographicCoordinates | MissingValue,
    ) -> TrueSolarTimeAdjustment: ...


@dataclass(frozen=True, slots=True)
class DisabledTrueSolarTimeStrategy:
    """Explicitly records no adjustment; no enabled formula is selected in M3."""

    manifest: CalendarDataManifest
    strategy_id: str = "true-solar-time-disabled"
    strategy_version: str = "1.0.0"

    def __post_init__(self) -> None:
        if CalendarCapability.TRUE_SOLAR_TIME not in self.manifest.capabilities:
            raise ValueError("true-solar-time manifest lacks required capability")

    def adjust(
        self,
        local_time: LocalDateTime,
        coordinates: GeographicCoordinates | MissingValue,
    ) -> TrueSolarTimeAdjustment:
        del coordinates
        return TrueSolarTimeAdjustment(
            local_time,
            int(timedelta(0).total_seconds()),
            False,
            self.strategy_id,
            self.strategy_version,
            self.manifest,
        )
