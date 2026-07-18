from decimal import Decimal

import pytest
from ai_bazi_backend.modules.rule_evaluation import (
    Compatibility,
    EffectiveStatus,
    RuleId,
    RuleParameter,
    RuleSetId,
    RuleVersionProtocol,
    SemanticVersion,
)
from hypothesis import given
from hypothesis import strategies as st


@given(st.integers(min_value=0), st.integers(min_value=0), st.integers(min_value=0))
def test_semantic_version_round_trip(major: int, minor: int, patch: int) -> None:
    version = SemanticVersion(major, minor, patch)
    assert tuple(int(item) for item in str(version).split(".")) == (major, minor, patch)


def test_duplicate_deterministic_parameters_are_rejected() -> None:
    with pytest.raises(ValueError, match="unique"):
        RuleVersionProtocol(
            rule_id=RuleId("placeholder-rule"),
            rule_set_id=RuleSetId("empty-ruleset"),
            version=SemanticVersion(0, 0, 0),
            status=EffectiveStatus.PROPOSED,
            compatibility=Compatibility.UNKNOWN,
            supersedes=None,
            sources=(),
            deterministic_parameters=(
                RuleParameter("parameter", Decimal("1")),
                RuleParameter("parameter", Decimal("2")),
            ),
        )


def test_published_rule_requires_governed_source() -> None:
    with pytest.raises(ValueError, match="governed sources"):
        RuleVersionProtocol(
            rule_id=RuleId("placeholder-rule"),
            rule_set_id=RuleSetId("empty-ruleset"),
            version=SemanticVersion(1, 0, 0),
            status=EffectiveStatus.PUBLISHED,
            compatibility=Compatibility.UNKNOWN,
            supersedes=None,
            sources=(),
            deterministic_parameters=(),
        )
