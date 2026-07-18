import json
from dataclasses import replace
from datetime import UTC, date, datetime
from pathlib import Path

import pytest
from ai_bazi_backend.modules.calendar_time import (
    CivilDate,
    DataSourceKind,
    DataSourceReference,
    LocalDateTime,
    NormalizedInstant,
    NormalizedTimePoint,
    TimeComputationStep,
    TimeComputationTimeline,
    TimeDerivationId,
    TimeNormalizationResult,
    TimeNormalizationStatus,
    TimeTimelineNode,
)
from ai_bazi_backend.modules.chart_calculation import (
    EarthlyBranch,
    ExplicitFourPillarsFixtureProvider,
    FourPillarsCalculationError,
    FourPillarsCalculationRequest,
    FourPillarsEngine,
    FourPillarsErrorCode,
    FourPillarsFixtureRecord,
    FourPillarsRuleManifest,
    HeavenlyStem,
    PillarKind,
    PillarRuleBinding,
    PillarValue,
    RuleAuthority,
    four_pillars_result_to_document,
)
from ai_bazi_backend.modules.rule_evaluation import (
    Compatibility,
    EffectiveStatus,
    RuleId,
    RuleSetId,
    RuleVersionProtocol,
    SemanticVersion,
    SourceReference,
)

ROOT = Path(__file__).resolve().parents[4]
FIXTURE_PATH = ROOT / "tests/fixtures/m4/candidate-golden-four-pillars.json"


def fixture_document() -> dict[str, object]:
    return json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))


def records() -> tuple[FourPillarsFixtureRecord, ...]:
    document = fixture_document()
    cases = document["cases"]
    assert isinstance(cases, list)
    built: list[FourPillarsFixtureRecord] = []
    for case in cases:
        assert isinstance(case, dict)
        raw_pillars = case["pillars"]
        assert isinstance(raw_pillars, list)
        pillars = tuple(
            PillarValue(
                PillarKind(item["kind"]),
                HeavenlyStem(item["stem"]),
                EarthlyBranch(item["branch"]),
            )
            for item in raw_pillars
            if isinstance(item, dict)
        )
        built.append(
            FourPillarsFixtureRecord(
                str(case["utcInstant"]),
                str(case["logicalDate"]),
                str(case["offsetCandidateId"]),
                pillars,
            )
        )
    return tuple(built)


def rule(
    kind: PillarKind, status: EffectiveStatus = EffectiveStatus.PUBLISHED
) -> PillarRuleBinding:
    source = SourceReference("m4-engineering-fixture", "1.0.0", f"case.{kind.value}")
    protocol = RuleVersionProtocol(
        RuleId(f"m4.fixture.{kind.value}"),
        RuleSetId("m4.engineering-fixture"),
        SemanticVersion(0, 1, 0),
        status,
        Compatibility.UNKNOWN,
        None,
        (source,),
        (),
    )
    return PillarRuleBinding(
        kind,
        protocol,
        "explicit-fixture-lookup",
        SemanticVersion(0, 1, 0),
        (
            "docs/adr/ADR-CAND-M4-001-FOUR-PILLARS-RULE-BINDING.md",
            "docs/adr/M2-DOMAIN-DECISIONS.md",
        ),
        (
            DataSourceReference(
                "m4-engineering-fixture",
                "1.0.0",
                DataSourceKind.ENGINEERING_FIXTURE,
            ),
        ),
    )


def provider(
    *, status: EffectiveStatus = EffectiveStatus.PUBLISHED
) -> ExplicitFourPillarsFixtureProvider:
    return ExplicitFourPillarsFixtureProvider(
        FourPillarsRuleManifest(
            "m4-engineering-fixture-v1",
            RuleAuthority.ENGINEERING_FIXTURE,
            tuple(rule(kind, status) for kind in PillarKind),
        ),
        records(),
    )


def normalization(record: FourPillarsFixtureRecord) -> TimeNormalizationResult:
    instant = datetime.fromisoformat(record.utc_instant)
    logical = date.fromisoformat(record.logical_date)
    point = NormalizedTimePoint(
        LocalDateTime(CivilDate(logical.year, logical.month, logical.day), 3, 4, 5),
        LocalDateTime(CivilDate(logical.year, logical.month, logical.day), 3, 4, 5),
        NormalizedInstant(instant, f"{record.logical_date}T03:04:05", 28_800),
        CivilDate(logical.year, logical.month, logical.day),
        record.offset_candidate_id,
    )
    return TimeNormalizationResult(
        TimeNormalizationStatus.EXACT,
        (point,),
        TimeComputationTimeline(
            "1.0.0",
            (
                TimeTimelineNode(
                    0,
                    TimeDerivationId(f"{record.offset_candidate_id}:normalized"),
                    TimeComputationStep.DAY_BOUNDARY_RESOLVED,
                    record.logical_date,
                    (),
                    "m3-test-manifest",
                    "1.0.0",
                ),
            ),
        ),
        datetime(2026, 1, 1, tzinfo=UTC),
        ("m3-test-manifest",),
    )


def request(record: FourPillarsFixtureRecord) -> FourPillarsCalculationRequest:
    return FourPillarsCalculationRequest(
        "m4-request-1",
        "snapshot-1",
        normalization(record),
        datetime(2026, 1, 1, tzinfo=UTC),
        (DataSourceReference("m3-normalization", "1.0.0", DataSourceKind.CALENDAR_DATASET),),
        allow_engineering_fixture=True,
    )


def test_candidate_fixture_set_is_explicitly_not_expert_approved() -> None:
    document = fixture_document()
    assert document["authority"] == "engineering_fixture"
    assert document["expertApproval"] == "pending"
    assert len(records()) == 4


@pytest.mark.parametrize("record", records())
def test_candidate_golden_cases_produce_all_four_pillars_with_evidence(
    record: FourPillarsFixtureRecord,
) -> None:
    result = FourPillarsEngine(provider()).calculate(request(record))
    assert tuple(pillar.kind for pillar in result.four_pillars.ordered()) == tuple(PillarKind)
    assert tuple((pillar.stem, pillar.branch) for pillar in result.four_pillars.ordered()) == tuple(
        (item.stem, item.branch) for item in record.pillars
    )
    assert all(pillar.evidence_ids for pillar in result.four_pillars.ordered())
    assert all(pillar.rule_version.adr_references for pillar in result.four_pillars.ordered())
    assert len(result.trace.evidence) == 5
    assert len(result.outputs) == 4


def test_same_input_and_versions_are_deterministic() -> None:
    engine = FourPillarsEngine(provider())
    calculation_request = request(records()[0])
    assert engine.calculate(calculation_request) == engine.calculate(calculation_request)


def test_document_mapping_preserves_rule_and_evidence_links() -> None:
    result = FourPillarsEngine(provider()).calculate(request(records()[0]))
    document = four_pillars_result_to_document(result)
    assert document["schemaVersion"] == "1.0.0"
    pillars = document["pillars"]
    assert isinstance(pillars, list)
    assert all(item["rule"]["adrReferences"] for item in pillars)
    assert all(item["evidenceIds"] for item in pillars)


def test_engineering_fixture_is_rejected_by_default() -> None:
    calculation_request = replace(request(records()[0]), allow_engineering_fixture=False)
    with pytest.raises(FourPillarsCalculationError) as captured:
        FourPillarsEngine(provider()).calculate(calculation_request)
    assert captured.value.code is FourPillarsErrorCode.RULE_AUTHORITY_NOT_APPROVED


def test_unpublished_rules_are_rejected() -> None:
    with pytest.raises(FourPillarsCalculationError) as captured:
        FourPillarsEngine(provider(status=EffectiveStatus.APPROVED)).calculate(
            request(records()[0])
        )
    assert captured.value.code is FourPillarsErrorCode.RULE_NOT_PUBLISHED


@pytest.mark.parametrize(
    "status,points",
    [
        (TimeNormalizationStatus.RANGE, (records()[0], records()[1])),
        (TimeNormalizationStatus.INDETERMINATE, ()),
    ],
)
def test_non_exact_normalization_is_rejected(
    status: TimeNormalizationStatus,
    points: tuple[FourPillarsFixtureRecord, ...],
) -> None:
    base = request(records()[0])
    normalized_points = tuple(normalization(item).points[0] for item in points)
    invalid = replace(
        base.normalized_time,
        status=status,
        points=normalized_points,
    )
    with pytest.raises(FourPillarsCalculationError) as captured:
        FourPillarsEngine(provider()).calculate(replace(base, normalized_time=invalid))
    assert captured.value.code is FourPillarsErrorCode.NORMALIZED_TIME_NOT_EXACT


def test_unknown_fixture_point_never_triggers_inference() -> None:
    point = replace(
        normalization(records()[0]).points[0],
        offset_candidate_id="not-in-fixture",
    )
    with pytest.raises(LookupError, match="not present"):
        provider().calculate(point)


def test_rule_binding_requires_adr_reference() -> None:
    original = rule(PillarKind.YEAR)
    with pytest.raises(ValueError, match="ADR"):
        replace(original, adr_references=())


def test_manifest_requires_all_pillars_in_order() -> None:
    with pytest.raises(ValueError, match="every pillar"):
        FourPillarsRuleManifest(
            "incomplete",
            RuleAuthority.ENGINEERING_FIXTURE,
            (rule(PillarKind.YEAR),),
        )


def test_manifest_rejects_mixed_rule_set_versions() -> None:
    bindings = tuple(rule(kind) for kind in PillarKind)
    changed_rule = replace(bindings[-1].rule, version=SemanticVersion(0, 2, 0))
    with pytest.raises(ValueError, match="one rule-set version"):
        FourPillarsRuleManifest(
            "mixed-versions",
            RuleAuthority.ENGINEERING_FIXTURE,
            (*bindings[:-1], replace(bindings[-1], rule=changed_rule)),
        )
