"""Ordered computation timeline for calendar/time derivations.

This is not the product Timeline aggregate and contains no fortune or interpretation node.
"""

from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import StrEnum

from .errors import CalendarTimeError, CalendarTimeErrorCode


class TimeComputationStep(StrEnum):
    INPUT_ACCEPTED = "input_accepted"
    CALENDAR_VALIDATED = "calendar_validated"
    TIME_ZONE_RESOLVED = "time_zone_resolved"
    UTC_CONVERTED = "utc_converted"
    TRUE_SOLAR_TIME_APPLIED = "true_solar_time_applied"
    DAY_BOUNDARY_RESOLVED = "day_boundary_resolved"


@dataclass(frozen=True, slots=True)
class TimeDerivationId:
    value: str

    def __post_init__(self) -> None:
        if not self.value.strip():
            raise ValueError("TimeDerivationId cannot be empty")


@dataclass(frozen=True, slots=True)
class TimeTimelineNode:
    sequence: int
    derivation_id: TimeDerivationId
    step: TimeComputationStep
    value: str
    parent_ids: tuple[TimeDerivationId, ...]
    source_id: str
    source_version: str

    def __post_init__(self) -> None:
        if self.sequence < 0:
            raise ValueError("timeline sequence cannot be negative")
        if not self.value.strip() or not self.source_id.strip() or not self.source_version.strip():
            raise ValueError("timeline node value and source metadata are required")


@dataclass(frozen=True, slots=True)
class TimeComputationTimeline:
    schema_version: str
    nodes: tuple[TimeTimelineNode, ...]

    def __post_init__(self) -> None:
        if not self.schema_version.strip() or not self.nodes:
            raise ValueError("timeline schema version and nodes are required")
        known: set[TimeDerivationId] = set()
        for expected, node in enumerate(self.nodes):
            if node.sequence != expected:
                raise CalendarTimeError(
                    CalendarTimeErrorCode.TIMELINE_INVALID,
                    "timeline.sequence",
                    "timeline sequence must be contiguous",
                )
            duplicate = node.derivation_id in known
            missing_parent = any(parent not in known for parent in node.parent_ids)
            if duplicate or missing_parent:
                raise CalendarTimeError(
                    CalendarTimeErrorCode.TIMELINE_INVALID,
                    "timeline.parents",
                    "timeline identities must be unique and parents must precede children",
                )
            known.add(node.derivation_id)


@dataclass(frozen=True, slots=True)
class NormalizedInstant:
    utc_instant: datetime
    local_time: str
    offset_seconds: int

    def __post_init__(self) -> None:
        if self.utc_instant.tzinfo is None or self.utc_instant.utcoffset() != timedelta(0):
            raise ValueError("normalized instant must be UTC")
        if not self.local_time.strip():
            raise ValueError("normalized instant requires its source local time")
