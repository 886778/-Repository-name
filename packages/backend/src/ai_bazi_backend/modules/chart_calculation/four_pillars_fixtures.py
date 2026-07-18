"""Explicit table provider for engineering and expert-governed fixture datasets.

This adapter performs no hidden calendar or Four Pillars inference.  A point not present
in the supplied immutable table is rejected.
"""

from dataclasses import dataclass

from ai_bazi_backend.modules.calendar_time import NormalizedTimePoint

from .four_pillars_engine import FourPillarsRuleManifest, PillarValue


@dataclass(frozen=True, slots=True)
class FourPillarsFixtureRecord:
    utc_instant: str
    logical_date: str
    offset_candidate_id: str
    pillars: tuple[PillarValue, ...]


@dataclass(frozen=True, slots=True)
class ExplicitFourPillarsFixtureProvider:
    manifest: FourPillarsRuleManifest
    records: tuple[FourPillarsFixtureRecord, ...]

    def __post_init__(self) -> None:
        keys = [
            (record.utc_instant, record.logical_date, record.offset_candidate_id)
            for record in self.records
        ]
        if len(keys) != len(set(keys)):
            raise ValueError("Four Pillars fixture keys must be unique")

    def calculate(self, point: NormalizedTimePoint) -> tuple[PillarValue, ...]:
        key = (
            point.instant.utc_instant.isoformat(),
            point.logical_date.to_date().isoformat(),
            point.offset_candidate_id,
        )
        for record in self.records:
            if (record.utc_instant, record.logical_date, record.offset_candidate_id) == key:
                return record.pillars
        raise LookupError("normalized point is not present in the explicit fixture dataset")
