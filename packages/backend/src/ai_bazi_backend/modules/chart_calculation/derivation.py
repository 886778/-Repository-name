"""Deterministic calculation derivation trace.

CalculationEvidence is a Chart Calculation trace value, not the Evidence Context's
Evidence entity and not an EvidenceBundle. The formal Evidence context may later cite a
frozen calculation snapshot published by this context.
"""

from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum

from ai_bazi_backend.modules.calendar_time import DataSourceReference, Uncertainty
from ai_bazi_backend.modules.rule_evaluation import RuleId, RuleSetId, SemanticVersion


@dataclass(frozen=True, slots=True)
class CalculationEvidenceId:
    value: str

    def __post_init__(self) -> None:
        if not self.value.strip():
            raise ValueError("CalculationEvidenceId cannot be empty")


class DerivationKind(StrEnum):
    INPUT_SNAPSHOT = "input_snapshot"
    INTERMEDIATE_VALUE = "intermediate_value"
    OUTPUT_VALUE = "output_value"


@dataclass(frozen=True, slots=True)
class DerivationValue:
    name: str
    value: str | int | bool

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise ValueError("derivation value name cannot be empty")


@dataclass(frozen=True, slots=True)
class CalculationEvidence:
    evidence_id: CalculationEvidenceId
    kind: DerivationKind
    value: DerivationValue
    rule_id: RuleId | None
    rule_set_id: RuleSetId
    rule_set_version: SemanticVersion
    algorithm_id: str
    algorithm_version: SemanticVersion
    sources: tuple[DataSourceReference, ...]
    calculated_at: datetime
    parent_ids: tuple[CalculationEvidenceId, ...]
    warning_codes: tuple[str, ...]
    uncertainties: tuple[Uncertainty, ...]

    def __post_init__(self) -> None:
        if self.calculated_at.tzinfo is None:
            raise ValueError("calculation time must include an explicit offset")
        if not self.algorithm_id.strip() or not self.sources:
            raise ValueError("algorithm identity and data sources are required")
        if self.kind is not DerivationKind.INPUT_SNAPSHOT and self.rule_id is None:
            raise ValueError("derived values require an explicit rule identity")


@dataclass(frozen=True, slots=True)
class CalculationOutput:
    output_id: str
    value: str | int | bool
    evidence_ids: tuple[CalculationEvidenceId, ...]

    def __post_init__(self) -> None:
        if not self.output_id.strip() or not self.evidence_ids:
            raise ValueError("every output must cite calculation evidence")


@dataclass(frozen=True, slots=True)
class CalculationTrace:
    evidence: tuple[CalculationEvidence, ...]

    def __post_init__(self) -> None:
        identities = [item.evidence_id for item in self.evidence]
        if len(identities) != len(set(identities)):
            raise ValueError("calculation evidence identities must be unique")
        known: set[CalculationEvidenceId] = set()
        for item in self.evidence:
            if any(parent not in known for parent in item.parent_ids):
                raise ValueError("parents must precede children in the derivation trace")
            known.add(item.evidence_id)

    def validate_outputs(self, outputs: tuple[CalculationOutput, ...]) -> None:
        known = {item.evidence_id for item in self.evidence}
        if any(
            evidence_id not in known for output in outputs for evidence_id in output.evidence_ids
        ):
            raise ValueError("calculation output references unknown evidence")
