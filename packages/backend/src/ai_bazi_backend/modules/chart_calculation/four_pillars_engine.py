"""Deterministic and authority-gated Four Pillars calculation foundation."""

from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import StrEnum
from typing import Protocol

from ai_bazi_backend.modules.calendar_time import (
    DataSourceReference,
    NormalizedTimePoint,
    TimeNormalizationResult,
    TimeNormalizationStatus,
)
from ai_bazi_backend.modules.rule_evaluation import (
    EffectiveStatus,
    RuleVersionProtocol,
    SemanticVersion,
)

from .derivation import (
    CalculationEvidence,
    CalculationEvidenceId,
    CalculationOutput,
    CalculationTrace,
    DerivationKind,
    DerivationValue,
)
from .four_pillars import (
    EarthlyBranch,
    FourPillars,
    HeavenlyStem,
    Pillar,
    PillarKind,
    PillarRuleVersion,
)


class FourPillarsErrorCode(StrEnum):
    NORMALIZED_TIME_NOT_EXACT = "normalized_time_not_exact"
    RULE_AUTHORITY_NOT_APPROVED = "rule_authority_not_approved"
    RULE_NOT_PUBLISHED = "rule_not_published"
    PROVIDER_RESULT_INCOMPLETE = "provider_result_incomplete"
    PROVIDER_RESULT_MISMATCH = "provider_result_mismatch"


class FourPillarsCalculationError(ValueError):
    def __init__(self, code: FourPillarsErrorCode, detail: str) -> None:
        super().__init__(detail)
        self.code = code
        self.detail = detail


class RuleAuthority(StrEnum):
    EXPERT_APPROVED = "expert_approved"
    ENGINEERING_FIXTURE = "engineering_fixture"


@dataclass(frozen=True, slots=True)
class PillarRuleBinding:
    kind: PillarKind
    rule: RuleVersionProtocol
    algorithm_id: str
    algorithm_version: SemanticVersion
    adr_references: tuple[str, ...]
    sources: tuple[DataSourceReference, ...]

    def __post_init__(self) -> None:
        if not self.algorithm_id.strip() or not self.sources:
            raise ValueError("pillar rule binding requires algorithm identity and sources")
        if not self.adr_references or any(not item.strip() for item in self.adr_references):
            raise ValueError("every pillar rule binding must cite an ADR")


@dataclass(frozen=True, slots=True)
class FourPillarsRuleManifest:
    manifest_id: str
    authority: RuleAuthority
    bindings: tuple[PillarRuleBinding, ...]

    def __post_init__(self) -> None:
        if not self.manifest_id.strip():
            raise ValueError("Four Pillars rule manifest identity is required")
        if tuple(binding.kind for binding in self.bindings) != tuple(PillarKind):
            raise ValueError("rule manifest requires one ordered binding for every pillar")
        rule_sets = {(binding.rule.rule_set_id, binding.rule.version) for binding in self.bindings}
        if len(rule_sets) != 1:
            raise ValueError("all pillar rules must belong to one rule-set version")


@dataclass(frozen=True, slots=True)
class PillarValue:
    kind: PillarKind
    stem: HeavenlyStem
    branch: EarthlyBranch


class FourPillarsProvider(Protocol):
    @property
    def manifest(self) -> FourPillarsRuleManifest: ...

    def calculate(self, point: NormalizedTimePoint) -> tuple[PillarValue, ...]: ...


@dataclass(frozen=True, slots=True)
class FourPillarsCalculationRequest:
    request_id: str
    calculation_snapshot_id: str
    normalized_time: TimeNormalizationResult
    calculated_at: datetime
    input_sources: tuple[DataSourceReference, ...]
    allow_engineering_fixture: bool = False

    def __post_init__(self) -> None:
        if not self.request_id.strip() or not self.calculation_snapshot_id.strip():
            raise ValueError("calculation request and snapshot identities are required")
        if self.calculated_at.tzinfo is None or self.calculated_at.utcoffset() != timedelta(0):
            raise ValueError("calculated_at must be an aware UTC instant")
        if not self.input_sources:
            raise ValueError("calculation request requires input sources")


@dataclass(frozen=True, slots=True)
class FourPillarsCalculationResult:
    four_pillars: FourPillars
    trace: CalculationTrace
    outputs: tuple[CalculationOutput, ...]
    rule_manifest_id: str
    authority: RuleAuthority

    def __post_init__(self) -> None:
        self.trace.validate_outputs(self.outputs)


@dataclass(frozen=True, slots=True)
class FourPillarsEngine:
    provider: FourPillarsProvider

    def calculate(self, request: FourPillarsCalculationRequest) -> FourPillarsCalculationResult:
        if request.normalized_time.status is not TimeNormalizationStatus.EXACT:
            raise FourPillarsCalculationError(
                FourPillarsErrorCode.NORMALIZED_TIME_NOT_EXACT,
                "Four Pillars calculation requires one explicitly normalized instant",
            )
        manifest = self.provider.manifest
        if (
            manifest.authority is RuleAuthority.ENGINEERING_FIXTURE
            and not request.allow_engineering_fixture
        ):
            raise FourPillarsCalculationError(
                FourPillarsErrorCode.RULE_AUTHORITY_NOT_APPROVED,
                "engineering fixtures cannot be used as an expert-approved calculation source",
            )
        if any(
            binding.rule.status is not EffectiveStatus.PUBLISHED for binding in manifest.bindings
        ):
            raise FourPillarsCalculationError(
                FourPillarsErrorCode.RULE_NOT_PUBLISHED,
                "all Four Pillars rules must be explicitly published before execution",
            )

        values = self.provider.calculate(request.normalized_time.points[0])
        if tuple(value.kind for value in values) != tuple(PillarKind):
            raise FourPillarsCalculationError(
                FourPillarsErrorCode.PROVIDER_RESULT_INCOMPLETE,
                "provider must return one ordered result for every pillar",
            )

        input_evidence = CalculationEvidence(
            CalculationEvidenceId(f"{request.request_id}:input"),
            DerivationKind.INPUT_SNAPSHOT,
            DerivationValue("calculation_snapshot_id", request.calculation_snapshot_id),
            None,
            manifest.bindings[0].rule.rule_set_id,
            manifest.bindings[0].rule.version,
            manifest.bindings[0].algorithm_id,
            manifest.bindings[0].algorithm_version,
            request.input_sources,
            request.calculated_at,
            (),
            (),
            (),
        )
        evidence = [input_evidence]
        pillars: list[Pillar] = []
        outputs: list[CalculationOutput] = []
        for value, binding in zip(values, manifest.bindings, strict=True):
            if value.kind is not binding.kind:
                raise FourPillarsCalculationError(
                    FourPillarsErrorCode.PROVIDER_RESULT_MISMATCH,
                    "provider pillar kind does not match its governed rule binding",
                )
            evidence_id = CalculationEvidenceId(f"{request.request_id}:pillar:{value.kind.value}")
            item = CalculationEvidence(
                evidence_id,
                DerivationKind.OUTPUT_VALUE,
                DerivationValue(
                    f"{value.kind.value}_pillar",
                    f"{value.stem.value}-{value.branch.value}",
                ),
                binding.rule.rule_id,
                binding.rule.rule_set_id,
                binding.rule.version,
                binding.algorithm_id,
                binding.algorithm_version,
                binding.sources,
                request.calculated_at,
                (input_evidence.evidence_id,),
                (),
                (),
            )
            rule_version = PillarRuleVersion(
                binding.rule.rule_id,
                binding.rule.rule_set_id,
                binding.rule.version,
                binding.algorithm_id,
                binding.algorithm_version,
                binding.adr_references,
            )
            pillar = Pillar(value.kind, value.stem, value.branch, rule_version, (evidence_id,))
            evidence.append(item)
            pillars.append(pillar)
            outputs.append(
                CalculationOutput(
                    f"four_pillars.{value.kind.value}",
                    f"{value.stem.value}-{value.branch.value}",
                    (evidence_id,),
                )
            )

        result = FourPillars(*pillars)
        return FourPillarsCalculationResult(
            result,
            CalculationTrace(tuple(evidence)),
            tuple(outputs),
            manifest.manifest_id,
            manifest.authority,
        )
