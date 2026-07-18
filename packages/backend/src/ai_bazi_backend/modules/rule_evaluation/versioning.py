"""Version protocol for expert-governed deterministic rules.

No Bazi rule definition or interpretation is included in this module.
"""

from dataclasses import dataclass
from decimal import Decimal
from enum import StrEnum


@dataclass(frozen=True, slots=True)
class RuleId:
    value: str

    def __post_init__(self) -> None:
        if not self.value.strip():
            raise ValueError("RuleId cannot be empty")


@dataclass(frozen=True, slots=True)
class RuleSetId:
    value: str

    def __post_init__(self) -> None:
        if not self.value.strip():
            raise ValueError("RuleSetId cannot be empty")


@dataclass(frozen=True, slots=True, order=True)
class SemanticVersion:
    major: int
    minor: int
    patch: int

    def __post_init__(self) -> None:
        if min(self.major, self.minor, self.patch) < 0:
            raise ValueError("semantic version components cannot be negative")

    def __str__(self) -> str:
        return f"{self.major}.{self.minor}.{self.patch}"


class EffectiveStatus(StrEnum):
    PROPOSED = "proposed"
    IN_REVIEW = "in_review"
    APPROVED = "approved"
    PUBLISHED = "published"
    DEPRECATED = "deprecated"
    RETIRED = "retired"


class Compatibility(StrEnum):
    BACKWARD_COMPATIBLE = "backward_compatible"
    BREAKING = "breaking"
    UNKNOWN = "unknown"


@dataclass(frozen=True, slots=True)
class SourceReference:
    source_id: str
    version: str
    locator: str

    def __post_init__(self) -> None:
        if not self.source_id.strip() or not self.version.strip() or not self.locator.strip():
            raise ValueError("rule source identity, version, and locator are required")


RuleParameterValue = str | int | bool | Decimal


@dataclass(frozen=True, slots=True)
class RuleParameter:
    key: str
    value: RuleParameterValue

    def __post_init__(self) -> None:
        if not self.key.strip():
            raise ValueError("rule parameter key cannot be empty")


@dataclass(frozen=True, slots=True)
class RuleVersionProtocol:
    rule_id: RuleId
    rule_set_id: RuleSetId
    version: SemanticVersion
    status: EffectiveStatus
    compatibility: Compatibility
    supersedes: SemanticVersion | None
    sources: tuple[SourceReference, ...]
    deterministic_parameters: tuple[RuleParameter, ...]

    def __post_init__(self) -> None:
        keys = [parameter.key for parameter in self.deterministic_parameters]
        if len(keys) != len(set(keys)):
            raise ValueError("rule parameter keys must be unique")
        if self.status is EffectiveStatus.PUBLISHED and not self.sources:
            raise ValueError("published rule versions require governed sources")
