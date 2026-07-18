"""Pure Chart Calculation input contracts.

The module deliberately contains no calendar conversion or Bazi formula.
"""

from dataclasses import dataclass
from enum import StrEnum

from ai_bazi_backend.modules.birth.contracts import CanonicalBirthInputSnapshot
from ai_bazi_backend.modules.rule_evaluation import SemanticVersion


@dataclass(frozen=True, slots=True)
class CalculationInputSnapshotId:
    value: str

    def __post_init__(self) -> None:
        if not self.value.strip():
            raise ValueError("CalculationInputSnapshotId cannot be empty")


@dataclass(frozen=True, slots=True)
class AlgorithmVersion:
    algorithm_id: str
    version: SemanticVersion
    data_versions: tuple[str, ...]

    def __post_init__(self) -> None:
        if not self.algorithm_id.strip() or not self.data_versions:
            raise ValueError("algorithm identity and data versions are required")
        if any(not item.strip() for item in self.data_versions):
            raise ValueError("algorithm data versions cannot be empty")


class CalculationPolicy(StrEnum):
    STRICT = "strict"
    ALLOW_PARTIAL = "allow_partial"


@dataclass(frozen=True, slots=True)
class CalculationInput:
    schema_version: str
    snapshot_id: CalculationInputSnapshotId
    canonical_birth_input: CanonicalBirthInputSnapshot
    policy: CalculationPolicy

    def __post_init__(self) -> None:
        if not self.schema_version.strip():
            raise ValueError("calculation input schema version is required")
