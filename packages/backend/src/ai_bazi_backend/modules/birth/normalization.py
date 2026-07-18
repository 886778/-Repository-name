"""Deterministic stage boundaries for birth-input normalization."""

from dataclasses import dataclass
from enum import StrEnum
from typing import Protocol

from .domain import CanonicalBirthInput, RawBirthInput, ValidatedBirthInput


class InputStage(StrEnum):
    RAW = "raw"
    VALIDATED = "validated"
    CANONICAL = "canonical"
    CALCULATION = "calculation"


class NormalizationErrorCode(StrEnum):
    INVALID_VALUE = "invalid_value"
    MISSING_REQUIRED_VALUE = "missing_required_value"
    AMBIGUOUS_VALUE = "ambiguous_value"
    UNCONFIRMED_VALUE = "unconfirmed_value"
    UNSUPPORTED_CALENDAR = "unsupported_calendar"
    SOURCE_VERSION_MISSING = "source_version_missing"


class DecisionMethod(StrEnum):
    USER_SELECTION = "user_selection"
    EXPLICIT_DEFAULT = "explicit_default"
    DATASET_RESOLUTION = "dataset_resolution"
    USER_OVERRIDE = "user_override"


@dataclass(frozen=True, slots=True)
class NormalizationError(Exception):
    code: NormalizationErrorCode
    stage: InputStage
    field: str
    message: str


@dataclass(frozen=True, slots=True)
class NormalizationDecision:
    decision_id: str
    field: str
    method: DecisionMethod
    source_reference: str
    source_version: str
    original_value: str | None
    selected_value: str
    overrideable: bool
    user_confirmed: bool

    def __post_init__(self) -> None:
        if not all(
            value.strip()
            for value in (
                self.decision_id,
                self.field,
                self.source_reference,
                self.source_version,
                self.selected_value,
            )
        ):
            raise ValueError("normalization decision metadata cannot be empty")
        if self.method is not DecisionMethod.USER_SELECTION and not self.user_confirmed:
            raise ValueError("automatic normalization must be explicit and confirmed")


@dataclass(frozen=True, slots=True)
class ValidationOutcome:
    value: ValidatedBirthInput
    decisions: tuple[NormalizationDecision, ...]


@dataclass(frozen=True, slots=True)
class CanonicalizationOutcome:
    value: CanonicalBirthInput
    decisions: tuple[NormalizationDecision, ...]


class BirthInputValidator(Protocol):
    def validate(self, raw_input: RawBirthInput) -> ValidationOutcome: ...


class BirthInputCanonicalizer(Protocol):
    def canonicalize(self, validated_input: ValidatedBirthInput) -> CanonicalizationOutcome: ...
