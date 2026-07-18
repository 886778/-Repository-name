"""Pure deterministic calculation-kernel port and a no-op architecture fixture."""

from dataclasses import dataclass
from datetime import datetime
from typing import Protocol

from ai_bazi_backend.modules.calendar_time import DataSourceReference
from ai_bazi_backend.modules.rule_evaluation import RuleSetId, SemanticVersion

from .derivation import (
    CalculationEvidence,
    CalculationEvidenceId,
    CalculationOutput,
    CalculationTrace,
    DerivationKind,
    DerivationValue,
)
from .domain import AlgorithmVersion, CalculationInput


@dataclass(frozen=True, slots=True)
class KernelRequest:
    calculation_input: CalculationInput
    algorithm: AlgorithmVersion
    rule_set_id: RuleSetId
    rule_set_version: SemanticVersion
    calculated_at: datetime
    source: DataSourceReference

    def __post_init__(self) -> None:
        if self.calculated_at.tzinfo is None:
            raise ValueError("kernel request time must be explicit and timezone-aware")


@dataclass(frozen=True, slots=True)
class KernelResult:
    outputs: tuple[CalculationOutput, ...]
    trace: CalculationTrace

    def __post_init__(self) -> None:
        self.trace.validate_outputs(self.outputs)


class CalculationKernel(Protocol):
    def calculate(self, request: KernelRequest) -> KernelResult: ...


class NoOpCalculationKernel:
    """Produces only a traceable input snapshot; it performs no Bazi calculation."""

    def calculate(self, request: KernelRequest) -> KernelResult:
        evidence = CalculationEvidence(
            evidence_id=CalculationEvidenceId(
                f"input:{request.calculation_input.snapshot_id.value}"
            ),
            kind=DerivationKind.INPUT_SNAPSHOT,
            value=DerivationValue(
                name="calculation_input_snapshot_id",
                value=request.calculation_input.snapshot_id.value,
            ),
            rule_id=None,
            rule_set_id=request.rule_set_id,
            rule_set_version=request.rule_set_version,
            algorithm_id=request.algorithm.algorithm_id,
            algorithm_version=request.algorithm.version,
            sources=(request.source,),
            calculated_at=request.calculated_at,
            parent_ids=(),
            warning_codes=("NO_OP_KERNEL",),
            uncertainties=request.calculation_input.canonical_birth_input.uncertainties,
        )
        return KernelResult(outputs=(), trace=CalculationTrace(evidence=(evidence,)))
