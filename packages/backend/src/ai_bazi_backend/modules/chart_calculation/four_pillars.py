"""Framework-free Four Pillars values.

These values represent deterministic chart output only.  They deliberately contain no
Five Elements, Ten Gods, strength, pattern, luck-cycle, or interpretation semantics.
"""

from dataclasses import dataclass
from enum import StrEnum

from ai_bazi_backend.modules.rule_evaluation import RuleId, RuleSetId, SemanticVersion

from .derivation import CalculationEvidenceId


class HeavenlyStem(StrEnum):
    JIA = "jia"
    YI = "yi"
    BING = "bing"
    DING = "ding"
    WU = "wu"
    JI = "ji"
    GENG = "geng"
    XIN = "xin"
    REN = "ren"
    GUI = "gui"


class EarthlyBranch(StrEnum):
    ZI = "zi"
    CHOU = "chou"
    YIN = "yin"
    MAO = "mao"
    CHEN = "chen"
    SI = "si"
    WU = "wu"
    WEI = "wei"
    SHEN = "shen"
    YOU = "you"
    XU = "xu"
    HAI = "hai"


class PillarKind(StrEnum):
    YEAR = "year"
    MONTH = "month"
    DAY = "day"
    HOUR = "hour"


@dataclass(frozen=True, slots=True)
class PillarRuleVersion:
    rule_id: RuleId
    rule_set_id: RuleSetId
    rule_set_version: SemanticVersion
    algorithm_id: str
    algorithm_version: SemanticVersion
    adr_references: tuple[str, ...]

    def __post_init__(self) -> None:
        if not self.algorithm_id.strip():
            raise ValueError("pillar algorithm identity is required")
        if not self.adr_references or any(not value.strip() for value in self.adr_references):
            raise ValueError("pillar rule versions must cite governing ADR records")


@dataclass(frozen=True, slots=True)
class Pillar:
    kind: PillarKind
    stem: HeavenlyStem
    branch: EarthlyBranch
    rule_version: PillarRuleVersion
    evidence_ids: tuple[CalculationEvidenceId, ...]

    def __post_init__(self) -> None:
        if not self.evidence_ids:
            raise ValueError("every pillar must cite calculation evidence")


@dataclass(frozen=True, slots=True)
class FourPillars:
    year: Pillar
    month: Pillar
    day: Pillar
    hour: Pillar

    def __post_init__(self) -> None:
        values = (self.year, self.month, self.day, self.hour)
        if tuple(value.kind for value in values) != tuple(PillarKind):
            raise ValueError("FourPillars must contain year, month, day, and hour in order")

    def ordered(self) -> tuple[Pillar, ...]:
        return (self.year, self.month, self.day, self.hour)
