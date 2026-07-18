import json
from pathlib import Path

import pytest
from ai_bazi_backend.modules.birth.contracts import (
    raw_birth_input_from_document,
    raw_birth_input_to_document,
)
from ai_bazi_backend.modules.birth.normalization import DecisionMethod, NormalizationDecision

ROOT = Path(__file__).resolve().parents[4]


def test_raw_birth_input_serialization_round_trip() -> None:
    document = json.loads((ROOT / "tests/fixtures/m2/normal-input.json").read_text())
    value = raw_birth_input_from_document(document)
    assert raw_birth_input_to_document(value) == document


def test_missing_time_serialization_round_trip() -> None:
    document = json.loads((ROOT / "tests/fixtures/m2/missing-time.json").read_text())
    value = raw_birth_input_from_document(document)
    assert raw_birth_input_to_document(value) == document


def test_automatic_normalization_requires_confirmation() -> None:
    with pytest.raises(ValueError, match="confirmed"):
        NormalizationDecision(
            decision_id="decision-1",
            field="timeZone",
            method=DecisionMethod.DATASET_RESOLUTION,
            source_reference="timezone-source",
            source_version="pending",
            original_value="raw-zone",
            selected_value="resolved-zone",
            overrideable=True,
            user_confirmed=False,
        )


def test_explicit_normalization_is_traceable_and_overrideable() -> None:
    decision = NormalizationDecision(
        decision_id="decision-1",
        field="timeZone",
        method=DecisionMethod.USER_OVERRIDE,
        source_reference="timezone-source",
        source_version="pending",
        original_value="raw-zone",
        selected_value="resolved-zone",
        overrideable=True,
        user_confirmed=True,
    )
    assert decision.overrideable
    assert decision.source_version == "pending"
