"""Stable document mapping for Calendar & Time normalization results."""

from typing import Any

from .normalization import TimeNormalizationResult


def time_normalization_result_to_document(value: TimeNormalizationResult) -> dict[str, Any]:
    return {
        "schemaVersion": value.timeline.schema_version,
        "status": value.status.value,
        "performedAt": value.performed_at.isoformat(),
        "providerManifestIds": list(value.provider_manifest_ids),
        "points": [
            {
                "civilLocalTime": point.civil_local_time.as_naive_datetime().isoformat(),
                "adjustedLocalTime": point.adjusted_local_time.as_naive_datetime().isoformat(),
                "utcInstant": point.instant.utc_instant.isoformat(),
                "offsetSeconds": point.instant.offset_seconds,
                "logicalDate": point.logical_date.to_date().isoformat(),
                "offsetCandidateId": point.offset_candidate_id,
            }
            for point in value.points
        ],
        "timeline": [
            {
                "sequence": node.sequence,
                "derivationId": node.derivation_id.value,
                "step": node.step.value,
                "value": node.value,
                "parentIds": [parent.value for parent in node.parent_ids],
                "sourceId": node.source_id,
                "sourceVersion": node.source_version,
            }
            for node in value.timeline.nodes
        ],
    }
