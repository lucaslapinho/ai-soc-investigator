#!/usr/bin/env python3
"""Validate the local SOC report contract. No network, subprocess or response actions."""
import argparse
import json
import re
from datetime import datetime
from pathlib import Path
from jsonschema import Draft202012Validator, FormatChecker
ROOT = Path(__file__).resolve().parents[1]
FORMATS = FormatChecker()

@FORMATS.checks("date-time", raises=(ValueError, TypeError))
def valid_datetime(value):
    if not isinstance(value, str):
        return True
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})", value):
        return False
    return datetime.fromisoformat(value.replace("Z", "+00:00")).tzinfo is not None
def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"Duplicate JSON key: {key}")
        result[key] = value
    return result
def read_json(path):
    p = Path(path)
    if p.stat().st_size > 10 * 1024 * 1024:
        raise ValueError("JSON exceeds the 10 MiB validation limit")
    return json.loads(p.read_text(encoding="utf-8"), object_pairs_hook=unique_object)
def timestamp(value):
    return datetime.fromisoformat(value.replace("Z", "+00:00"))
def semantic_errors(doc):
    errors = []
    def check(condition, message):
        if not condition:
            errors.append(message)
    def index(items, label):
        keys = [x["id"] for x in items]
        check(len(keys) == len(set(keys)), f"Duplicate IDs in {label}")
        return {x["id"]: x for x in items}
    sources = index(doc["sources"], "sources")
    evidence = index(doc["evidence"]["items"], "evidence")
    entities = index(doc["entities"], "entities")
    for label in ("queries", "timeline", "gaps", "actions", "references"):
        index(doc[label], label)
    tenant = doc["context"]["tenant_ref"]
    def ids(values, known, label):
        for value in values:
            check(value in known, f"{label}: unresolved ID {value}")
    def times(original, utc, label):
        if original and utc:
            try:
                parsed = datetime.fromisoformat(original.replace("Z", "+00:00"))
            except ValueError:
                return
            if parsed.tzinfo:
                check(parsed == timestamp(utc), f"{label}: original time and UTC disagree")
    for source in sources.values():
        check(source["tenant_ref"] == tenant, f"{source['id']}: cross-tenant source")
    for ev in evidence.values():
        ids([ev["source_id"]], sources, ev["id"])
        if ev["source_id"] in sources and ev["kind"] == "Observation":
            check(sources[ev["source_id"]]["access_status"] != "Unavailable",
                  f"{ev['id']}: observed evidence from unavailable source")
        times(ev["original_time"], ev["observed_at"], ev["id"])
    for key in ("supporting_ids", "opposing_ids"):
        ids(doc["evidence"][key], evidence, key)
    check(not(set(doc["evidence"]["supporting_ids"]) & set(doc["evidence"]["opposing_ids"])),
          "Supporting/opposing IDs overlap; describe distinct observations or use hypotheses")
    ids(doc["justification"]["evidence_ids"], evidence, "justification")
    ids(doc["impact"]["evidence_ids"], evidence, "impact")
    for ent in entities.values():
        check(ent["tenant_ref"] == tenant, f"{ent['id']}: cross-tenant entity")
        ids(ent["evidence_ids"], evidence, ent["id"])
    for query in doc["queries"]:
        check(query["tenant_ref"] == tenant, f"{query['id']}: cross-tenant query")
        ids([query["source_id"]], sources, query["id"])
    for event in doc["timeline"]:
        ids(event["entity_ids"], entities, event["id"])
        ids(event["evidence_ids"], evidence, event["id"])
        times(event["original_time"], event["time_utc"], event["id"])
        if event["precision"] == "Exact":
            check(event["time_utc"] is not None, f"{event['id']}: Exact time needs UTC")
    for technique in doc["attack"]:
        ids(technique["evidence_ids"], evidence, technique["id"])
        expected = "https://attack.mitre.org/techniques/" + technique["id"].replace(".", "/") + "/"
        check(technique["source_url"] == expected, f"{technique['id']}: ATT&CK URL mismatch")
    for key in ("confirmed_entity_ids", "potential_entity_ids"):
        ids(doc["scope"][key], entities, key)
    check(not(set(doc["scope"]["confirmed_entity_ids"]) & set(doc["scope"]["potential_entity_ids"])),
          "Scope has same entity as both confirmed and potential")
    check(timestamp(doc["updated_at"]) >= timestamp(doc["created_at"]),
          "updated_at precedes created_at")
    for act in doc["actions"]:
        check(act["tenant_ref"] == tenant, f"{act['id']}: cross-tenant action")
        ids(act["target_entity_ids"], entities, act["id"])
        ids(act["justification_evidence_ids"], evidence, act["id"])
        approval = act["approval"]
        execution = act["execution"]
        if approval:
            check(approval["tenant_ref"] == tenant, f"{act['id']}: approval tenant mismatch")
            check(set(approval["target_entity_ids"]) == set(act["target_entity_ids"]),
                  f"{act['id']}: approval targets mismatch")
            if approval["expires_at"]:
                check(timestamp(approval["expires_at"]) >= timestamp(approval["approved_at"]),
                      f"{act['id']}: approval expires before decision")
        if execution:
            ids(execution["verification_evidence_ids"], evidence, act["id"])
            check(timestamp(execution["started_at"]) >= timestamp(approval["approved_at"]),
                  f"{act['id']}: execution predates approval")
            if approval["expires_at"]:
                check(timestamp(execution["started_at"]) <= timestamp(approval["expires_at"]),
                      f"{act['id']}: execution after approval expired")
            if execution["finished_at"]:
                check(timestamp(execution["finished_at"]) >= timestamp(execution["started_at"]),
                      f"{act['id']}: execution finishes before start")
            if act["status"] == "Executed":
                for key in execution["verification_evidence_ids"]:
                    if key in evidence:
                        check(evidence[key]["kind"] == "Observation",
                              f"{act['id']}: verification cannot be only inference/hypothesis")
    return errors
def validate(doc, schema=None):
    schema = schema if schema is not None else read_json(ROOT / "schemas/incident.schema.json")
    Draft202012Validator.check_schema(schema)
    errors = [f"{'/'.join(map(str,e.absolute_path)) or '/'}: {e.message}"
              for e in Draft202012Validator(schema, format_checker=FORMATS).iter_errors(doc)]
    if not errors:
        errors.extend(semantic_errors(doc))
    return errors
def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("report", type=Path)
    args = parser.parse_args()
    try:
        errors = validate(read_json(args.report))
    except (OSError, ValueError) as exc:
        print(f"FAIL: {exc}")
        return 1
    for error in errors:
        print(f"FAIL: {error}")
    if not errors:
        print("PASS: JSON Schema and local semantic invariants (not evidence authenticity or operational safety)")
    return int(bool(errors))
if __name__ == "__main__":
    raise SystemExit(main())
