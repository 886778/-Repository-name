"""Published immutable Birth snapshots and JSON boundary mappings."""

from dataclasses import dataclass
from typing import Any

from ai_bazi_backend.modules.calendar_time import (
    CalendarDate,
    ClockTime,
    DataSourceKind,
    DataSourceReference,
    GeographicCoordinates,
    MissingReason,
    MissingValue,
    TimeRange,
    TimeZoneReference,
    Uncertainty,
)

from .domain import (
    BirthInputId,
    CanonicalBirthInput,
    ConfirmationStatus,
    RawBirthInput,
    RawText,
    RuleSexMarker,
)


@dataclass(frozen=True, slots=True)
class CanonicalBirthInputSnapshot:
    """Public snapshot value; it is not the BirthInput internal entity."""

    schema_version: str
    input_id: BirthInputId
    birth_date: CalendarDate
    birth_time: ClockTime | TimeRange | MissingValue
    time_zone: TimeZoneReference
    coordinates: GeographicCoordinates | MissingValue
    rule_sex_marker: RuleSexMarker
    source_chain: tuple[DataSourceReference, ...]
    uncertainties: tuple[Uncertainty, ...]
    confirmation: ConfirmationStatus

    @classmethod
    def publish(cls, value: CanonicalBirthInput) -> CanonicalBirthInputSnapshot:
        return cls(
            schema_version=value.schema_version,
            input_id=value.input_id,
            birth_date=value.birth_date,
            birth_time=value.birth_time,
            time_zone=value.time_zone,
            coordinates=value.coordinates,
            rule_sex_marker=value.rule_sex_marker,
            source_chain=value.source_chain,
            uncertainties=value.uncertainties,
            confirmation=value.confirmation,
        )


def raw_birth_input_to_document(value: RawBirthInput) -> dict[str, Any]:
    def raw_or_missing(item: RawText | MissingValue) -> str | dict[str, str]:
        return item.value if isinstance(item, RawText) else {"reason": item.reason.value}

    return {
        "schemaVersion": value.schema_version,
        "inputId": value.input_id.value,
        "calendar": value.calendar_text.value,
        "date": value.date_text.value,
        "time": raw_or_missing(value.time_text),
        "place": raw_or_missing(value.place_text),
        "timeZone": raw_or_missing(value.time_zone_text),
        "ruleSexMarker": value.rule_sex_marker.value,
        "source": {
            "sourceId": value.source.source_id,
            "version": value.source.version,
            "kind": value.source.kind.value,
        },
        "confirmation": value.confirmation.value,
    }


def raw_birth_input_from_document(document: dict[str, Any]) -> RawBirthInput:
    def raw_or_missing(item: object) -> RawText | MissingValue:
        if isinstance(item, str):
            return RawText(item)
        if isinstance(item, dict) and isinstance(item.get("reason"), str):
            return MissingValue(MissingReason(item["reason"]))
        raise ValueError("raw input field must be text or an explicit missing value")

    source = document["source"]
    if not isinstance(source, dict):
        raise ValueError("source must be an object")
    return RawBirthInput(
        schema_version=str(document["schemaVersion"]),
        input_id=BirthInputId(str(document["inputId"])),
        calendar_text=RawText(str(document["calendar"])),
        date_text=RawText(str(document["date"])),
        time_text=raw_or_missing(document["time"]),
        place_text=raw_or_missing(document["place"]),
        time_zone_text=raw_or_missing(document["timeZone"]),
        rule_sex_marker=RuleSexMarker(str(document["ruleSexMarker"])),
        source=DataSourceReference(
            source_id=str(source["sourceId"]),
            version=str(source["version"]),
            kind=DataSourceKind(str(source["kind"])),
        ),
        confirmation=ConfirmationStatus(str(document["confirmation"])),
    )
