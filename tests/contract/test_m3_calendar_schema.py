import json
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[2]
SCHEMA_PATH = ROOT / "packages/contracts/schemas/m3/time-normalization-result.schema.json"
FIXTURE_PATH = ROOT / "tests/fixtures/m3/time-normalization-result.json"


def test_normalization_document_matches_m3_schema() -> None:
    document = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    Draft202012Validator(schema, format_checker=FormatChecker()).validate(document)
    assert document["points"][0]["utcInstant"] == "2000-01-01T19:04:05+00:00"


def test_m3_schema_identity_is_stable() -> None:
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    assert schema["$id"].endswith("/1.0.0")
    assert schema["properties"]["schemaVersion"]["const"] == "1.0.0"
