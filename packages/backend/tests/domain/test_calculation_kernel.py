from datetime import UTC, datetime
from decimal import Decimal

import pytest
from ai_bazi_backend.modules.birth import (
    BirthInputId,
    CanonicalBirthInput,
    ConfirmationStatus,
    RuleSexMarker,
)
from ai_bazi_backend.modules.birth.contracts import CanonicalBirthInputSnapshot
from ai_bazi_backend.modules.calendar_time import (
    CalendarDate,
    CalendarType,
    ClockTime,
    CoordinatePrecision,
    DataSourceKind,
    DataSourceReference,
    DatePrecision,
    GeographicCoordinates,
    TimePrecision,
    TimeZoneIdentifier,
    TimeZoneReference,
    TimeZoneResolution,
)
from ai_bazi_backend.modules.chart_calculation import (
    AlgorithmVersion,
    CalculationEvidence,
    CalculationEvidenceId,
    CalculationInput,
    CalculationInputSnapshotId,
    CalculationOutput,
    CalculationPolicy,
    CalculationTrace,
    DerivationKind,
    KernelRequest,
    NoOpCalculationKernel,
)
from ai_bazi_backend.modules.chart_calculation.derivation import DerivationValue
from ai_bazi_backend.modules.rule_evaluation import RuleId, RuleSetId, SemanticVersion


def request() -> KernelRequest:
    source = DataSourceReference("fixture", "1.0.0", DataSourceKind.USER_PROVIDED)
    canonical = CanonicalBirthInput(
        schema_version="1.0.0",
        input_id=BirthInputId("birth-input-1"),
        birth_date=CalendarDate(2000, 1, 2, CalendarType.GREGORIAN, DatePrecision.DAY),
        birth_time=ClockTime(3, 4, None, TimePrecision.MINUTE),
        time_zone=TimeZoneReference(
            TimeZoneResolution.RESOLVED,
            TimeZoneIdentifier("Asia/Shanghai"),
            (),
            "timezone-source",
            "pending",
        ),
        coordinates=GeographicCoordinates(
            Decimal("39.9"),
            Decimal("116.4"),
            CoordinatePrecision.LOCALITY,
            "location-source",
            "pending",
        ),
        rule_sex_marker=RuleSexMarker.UNSPECIFIED,
        source_chain=(source,),
        uncertainties=(),
        confirmation=ConfirmationStatus.CONFIRMED,
    )
    return KernelRequest(
        calculation_input=CalculationInput(
            "1.0.0",
            CalculationInputSnapshotId("snapshot-1"),
            CanonicalBirthInputSnapshot.publish(canonical),
            CalculationPolicy.STRICT,
        ),
        algorithm=AlgorithmVersion("noop-kernel", SemanticVersion(0, 0, 0), ("none",)),
        rule_set_id=RuleSetId("empty-ruleset"),
        rule_set_version=SemanticVersion(0, 0, 0),
        calculated_at=datetime(2026, 1, 1, tzinfo=UTC),
        source=source,
    )


def test_noop_kernel_is_deterministic() -> None:
    kernel = NoOpCalculationKernel()
    assert kernel.calculate(request()) == kernel.calculate(request())


def test_noop_kernel_produces_no_bazi_result() -> None:
    result = NoOpCalculationKernel().calculate(request())
    assert result.outputs == ()
    assert len(result.trace.evidence) == 1
    assert result.trace.evidence[0].warning_codes == ("NO_OP_KERNEL",)


def test_output_cannot_bypass_evidence_trace() -> None:
    trace = CalculationTrace(evidence=NoOpCalculationKernel().calculate(request()).trace.evidence)
    output = CalculationOutput("unimplemented-output", "value", (CalculationEvidenceId("missing"),))
    with pytest.raises(ValueError, match="unknown evidence"):
        trace.validate_outputs((output,))


def test_derivation_parent_must_precede_child() -> None:
    req = request()
    with pytest.raises(ValueError, match="precede"):
        CalculationTrace(
            evidence=(
                CalculationEvidence(
                    CalculationEvidenceId("child"),
                    DerivationKind.INTERMEDIATE_VALUE,
                    DerivationValue("placeholder", "value"),
                    RuleId("placeholder-rule"),
                    req.rule_set_id,
                    req.rule_set_version,
                    req.algorithm.algorithm_id,
                    req.algorithm.version,
                    (req.source,),
                    req.calculated_at,
                    (CalculationEvidenceId("parent"),),
                    (),
                    (),
                ),
            )
        )


def test_kernel_rejects_implicit_system_time() -> None:
    req = request()
    with pytest.raises(ValueError, match="timezone-aware"):
        KernelRequest(
            req.calculation_input,
            req.algorithm,
            req.rule_set_id,
            req.rule_set_version,
            datetime(2026, 1, 1),
            req.source,
        )
