"""Stable document mapping for Four Pillars calculation results."""

from .four_pillars_engine import FourPillarsCalculationResult

type JsonValue = None | bool | int | float | str | list[JsonValue] | dict[str, JsonValue]


def four_pillars_result_to_document(result: FourPillarsCalculationResult) -> dict[str, JsonValue]:
    return {
        "schemaVersion": "1.0.0",
        "ruleManifestId": result.rule_manifest_id,
        "authority": result.authority.value,
        "pillars": [
            {
                "kind": pillar.kind.value,
                "stem": pillar.stem.value,
                "branch": pillar.branch.value,
                "rule": {
                    "ruleId": pillar.rule_version.rule_id.value,
                    "ruleSetId": pillar.rule_version.rule_set_id.value,
                    "ruleSetVersion": str(pillar.rule_version.rule_set_version),
                    "algorithmId": pillar.rule_version.algorithm_id,
                    "algorithmVersion": str(pillar.rule_version.algorithm_version),
                    "adrReferences": list(pillar.rule_version.adr_references),
                },
                "evidenceIds": [item.value for item in pillar.evidence_ids],
            }
            for pillar in result.four_pillars.ordered()
        ],
        "evidence": [
            {
                "evidenceId": item.evidence_id.value,
                "kind": item.kind.value,
                "name": item.value.name,
                "value": item.value.value,
                "ruleId": item.rule_id.value if item.rule_id else None,
                "ruleSetId": item.rule_set_id.value,
                "ruleSetVersion": str(item.rule_set_version),
                "algorithmId": item.algorithm_id,
                "algorithmVersion": str(item.algorithm_version),
                "calculatedAt": item.calculated_at.isoformat(),
                "parentIds": [parent.value for parent in item.parent_ids],
                "sources": [
                    {
                        "sourceId": source.source_id,
                        "version": source.version,
                        "kind": source.kind.value,
                    }
                    for source in item.sources
                ],
            }
            for item in result.trace.evidence
        ],
        "outputs": [
            {
                "outputId": output.output_id,
                "value": output.value,
                "evidenceIds": [item.value for item in output.evidence_ids],
            }
            for output in result.outputs
        ],
    }
