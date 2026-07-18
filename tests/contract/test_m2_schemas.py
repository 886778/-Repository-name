import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[2]
SCHEMA_ROOT = ROOT / "packages/contracts/schemas/m2"
FIXTURE_ROOT = ROOT / "tests/fixtures/m2"


def load(name: str, root: Path) -> object:
    return json.loads((root / name).read_text(encoding="utf-8"))


@pytest.mark.parametrize(
    ("fixture", "schema"),
    [
        ("normal-input.json", "raw-birth-input.schema.json"),
        ("missing-time.json", "raw-birth-input.schema.json"),
        ("boundary-date.json", "raw-birth-input.schema.json"),
        ("ambiguous-timezone.json", "calculation-input.schema.json"),
        ("evidence-chain.json", "calculation-trace.schema.json"),
    ],
)
def test_valid_fixtures_match_versioned_schema(fixture: str, schema: str) -> None:
    validator = Draft202012Validator(load(schema, SCHEMA_ROOT), format_checker=FormatChecker())
    validator.validate(load(fixture, FIXTURE_ROOT))


def test_invalid_fixture_is_rejected() -> None:
    validator = Draft202012Validator(load("raw-birth-input.schema.json", SCHEMA_ROOT))
    errors = list(validator.iter_errors(load("invalid-input.json", FIXTURE_ROOT)))
    assert errors


def test_schema_compatibility_manifest_covers_current_versions() -> None:
    manifest = load("compatibility.json", SCHEMA_ROOT)
    assert isinstance(manifest, dict)
    schemas = manifest["schemas"]
    for entry in schemas.values():
        assert entry["current"] in entry["readable"]


def test_schema_documents_use_stable_major_version() -> None:
    for path in SCHEMA_ROOT.glob("*.schema.json"):
        schema = json.loads(path.read_text(encoding="utf-8"))
        assert schema["$id"].endswith("/1.0.0")
        assert schema["properties"]["schemaVersion"]["const"] == "1.0.0"
