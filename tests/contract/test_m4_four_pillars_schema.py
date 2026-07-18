import json
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[2]


def validate(schema_name: str, fixture_name: str) -> dict[str, object]:
    schema = json.loads(
        (ROOT / f"packages/contracts/schemas/m4/{schema_name}").read_text(encoding="utf-8")
    )
    document = json.loads((ROOT / f"tests/fixtures/m4/{fixture_name}").read_text(encoding="utf-8"))
    Draft202012Validator(schema, format_checker=FormatChecker()).validate(document)
    return document


def test_candidate_golden_fixture_schema_is_stable() -> None:
    document = validate(
        "candidate-golden-four-pillars.schema.json",
        "candidate-golden-four-pillars.json",
    )
    assert document["schemaVersion"] == "1.0.0"
    assert document["expertApproval"] == "pending"
    cases = document["cases"]
    assert isinstance(cases, list)
    assert len(cases) == 4


def test_four_pillars_result_schema_identity_is_stable() -> None:
    schema = json.loads(
        (ROOT / "packages/contracts/schemas/m4/four-pillars-result.schema.json").read_text(
            encoding="utf-8"
        )
    )
    assert schema["$id"].endswith("/1.0.0")
    assert schema["properties"]["schemaVersion"]["const"] == "1.0.0"


def test_four_pillars_result_fixture_matches_contract() -> None:
    document = validate("four-pillars-result.schema.json", "four-pillars-result.json")
    pillars = document["pillars"]
    evidence = document["evidence"]
    assert isinstance(pillars, list)
    assert isinstance(evidence, list)
    evidence_ids = {item["evidenceId"] for item in evidence}
    assert all(set(item["evidenceIds"]) <= evidence_ids for item in pillars)
