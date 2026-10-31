#!/usr/bin/env python3
"""Build an offline, training-only collection plan; never collect or solve tasks.

Reads only the normalized train inputs/contracts plus membership/curation
metadata. No model/API/backend/SQL execution occurs. Administrative queue and
receipt requirements must not be serialized into teacher model prompts.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict, deque
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
INPUT_FIELDS = {"task_id", "domain", "system_prompt", "user_prompt", "selected_tools", "restricted_tools"}
DOMAIN_HINTS = {
    "calendar": [
        "Preserve the supplied timezone, date interpretation, event duration and recurrence rules.",
        "Record actual free/busy and existing-event observations before conditional scheduling or migration.",
        "Capture the exact returned IDs for calendars, events, ACL rules and watches; do not infer successful writes.",
    ],
    "csm": [
        "Resolve the requested case, account, contact and product from actual search results.",
        "Preserve case status, priority, ownership, entitlement, SLA and knowledge-link policy constraints.",
        "Record each observed link/update result and preserve failed or ambiguous branches for review.",
    ],
    "drive": [
        "Distinguish a file, folder, shared drive, revision, comment and permission ID.",
        "Retain exact observations for conditional access changes, revision retention and document copies.",
        "Record export/download tool results honestly; do not claim file contents were saved without evidence.",
    ],
    "email": [
        "Keep drafts, sent messages and threads distinct; an unsent draft is not a sent email.",
        "Use the real tool schema for aliases, forwarding, filters and vacation settings; preserve verification rules.",
        "Record the actual attachment/message data supplied by tools rather than reconstructing a promised attachment.",
    ],
    "hr": [
        "Resolve employees, HR profiles, services, groups and cases using visible tool results.",
        "Preserve HR access, assignment, case-task, checklist and notification policies from the task system prompt.",
        "Record whether requested state changes succeeded; do not infer that a notification or assignment completed.",
    ],
    "hybrid": [
        "Use an isolated reset covering every domain required by the workflow.",
        "Track domain/tool namespaces and IDs explicitly; similarly named users or records may belong to different systems.",
        "Preserve observations supporting each cross-domain handoff; a successful change in one system does not certify the whole task.",
    ],
    "itsm": [
        "Identify the intended incident, problem, user, configuration item and SLA from actual tool observations.",
        "Retain priority/state/assignment justification only when it is present in policy and observations.",
        "Record all required incident/problem/CI updates and notification outcomes, including backend errors.",
    ],
    "teams": [
        "Distinguish tenant, team, channel, group, chat, member, role, tab, call and virtual-event identifiers.",
        "Observe existing membership, installed apps and channel state before idempotent create/update branches.",
        "Record actual publication, messaging and call results; initiating a call does not prove a human conversation occurred.",
    ],
}


class QueueError(ValueError):
    pass


def canonical_bytes(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False,
                      allow_nan=False).encode("utf-8")


def canonical_sha256(value):
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def file_sha256(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def read_jsonl(path):
    records = []
    with Path(path).open() as handle:
        for number, line in enumerate(handle, 1):
            if not line.strip():
                continue
            value = json.loads(line)
            if not isinstance(value, dict):
                raise QueueError(f"{Path(path).name}:{number} must contain an object")
            records.append((number, value))
    return records


def load_training_sources():
    split_path = ROOT / "data/metadata/split_manifest.json"
    split = json.loads(split_path.read_text())
    expected = split["task_ids"]["train"]
    if len(expected) != 128 or len(set(expected)) != 128 or split["counts"]["train"] != 128:
        raise QueueError("Expected the frozen 128-task training membership")
    # IDs only; no held-out task payload is opened.
    excluded = set(split["task_ids"]["development"] + split["task_ids"]["final_test"])
    excluded |= set(split.get("excluded_reserve_ids", [])) | set(split.get("quarantined_ids", []))
    if set(expected) & excluded:
        raise QueueError("Training IDs overlap held-out/excluded membership")
    normalized = json.loads((ROOT / "data/metadata/normalization_manifest.json").read_text())
    paths = {
        "training_inputs": ROOT / "data/task_inputs/train.jsonl",
        "training_contracts": ROOT / "data/evaluator_only/train.jsonl",
    }
    for path in paths.values():
        relative = path.relative_to(ROOT).as_posix()
        if normalized["working_file_sha256"].get(relative) != file_sha256(path):
            raise QueueError(f"Normalized source hash mismatch: {relative}")
    inputs, line_numbers = {}, {}
    for line_number, record in read_jsonl(paths["training_inputs"]):
        task_id = record.get("task_id")
        if task_id not in expected or task_id in inputs or set(record) != INPUT_FIELDS:
            raise QueueError("Input file has non-training, duplicate or unexpected fields")
        if record.get("domain") not in DOMAIN_HINTS:
            raise QueueError("Unknown training domain")
        tools = record.get("selected_tools")
        if not isinstance(tools, list) or any(not isinstance(name, str) or not name for name in tools):
            raise QueueError("selected_tools must contain actual declared tool names")
        if len(set(tools)) != len(tools):
            raise QueueError("Repeated tool names remain in normalized inputs")
        inputs[task_id], line_numbers[task_id] = record, line_number
    contracts = {}
    for line_number, record in read_jsonl(paths["training_contracts"]):
        task_id = record.get("task_id")
        if task_id not in expected or task_id in contracts:
            raise QueueError("Contract file has duplicate or non-training membership")
        if {key: record.get(key) for key in INPUT_FIELDS} != inputs.get(task_id):
            raise QueueError("Input/contract model-visible fields differ")
        verifiers = record.get("verifiers")
        if not isinstance(verifiers, list) or not verifiers or any(not isinstance(v, dict) for v in verifiers):
            raise QueueError("Every task needs a nonempty normalized verifier list")
        names = [v.get("name") for v in verifiers]
        if any(not isinstance(n, str) or not n for n in names) or len(set(names)) != len(names):
            raise QueueError("Verifier names must be normalized and unique")
        contracts[task_id] = {
            "contract_source_line": line_number,
            "required_checks_total": len(verifiers),
            "verifier_contract_sha256": canonical_sha256(verifiers),
        }
    if set(inputs) != set(expected) or set(contracts) != set(expected):
        raise QueueError("Training files do not exactly cover the frozen membership")
    groups = json.loads((ROOT / "data/metadata/workflow_groups.json").read_text())
    task_to_group = {}
    for group in groups["groups"]:
        if group["active_role"] != "train":
            continue
        for task_id in group["active_task_ids"]:
            if task_id not in expected or task_id in task_to_group:
                raise QueueError("Workflow groups have duplicate/non-training IDs")
            task_to_group[task_id] = group["group_id"]
    if set(task_to_group) != set(expected):
        raise QueueError("Audited training workflow groups do not cover every task")
    holds = json.loads((ROOT / "data/metadata/quality_holds.json").read_text())
    held_training_ids = {row["task_id"] for row in holds.get("tasks", []) if row["task_id"] in inputs}
    if held_training_ids:
        raise QueueError("An unresolved quality hold intersects training; review before creating an executable queue")
    return inputs, contracts, line_numbers, task_to_group, paths, split_path


def collection_order(inputs, task_to_group):
    """Cover one task per audited family first; interleave domains without outcomes."""
    families = defaultdict(list)
    for task_id, group in task_to_group.items():
        families[group].append(task_id)
    leaders = {min(ids) for ids in families.values()}
    ordered = []
    for phase, candidates in (("FIRST_FAMILY_COVERAGE", leaders),
                              ("ADDITIONAL_FAMILY_MEMBER", set(inputs) - leaders)):
        per_domain = defaultdict(list)
        for task_id in candidates:
            per_domain[inputs[task_id]["domain"]].append(task_id)
        queues = {
            domain: deque(sorted(ids, key=lambda task_id: (task_to_group[task_id], task_id)))
            for domain, ids in per_domain.items()
        }
        while any(queues.values()):
            for domain in sorted(queues):
                if queues[domain]:
                    ordered.append((queues[domain].popleft(), phase))
    if len(ordered) != len(inputs) or len({task for task, _ in ordered}) != len(inputs):
        raise QueueError("Collection-order partition failed")
    return ordered


def build_artifacts():
    inputs, contracts, lines, task_to_group, paths, split_path = load_training_sources()
    rows, receipt_rows = [], []
    for position, (task_id, phase) in enumerate(collection_order(inputs, task_to_group), 1):
        source = inputs[task_id]
        input_hash = canonical_sha256(source)
        rows.append({
            "task_id": task_id, "domain": source["domain"], "role": "train",
            "workflow_group_id": task_to_group[task_id], "queue_order": position,
            "coverage_phase": phase, "status": "NOT_COLLECTED",
            "required_tool_names": source["selected_tools"],
            "source_input_file": "data/task_inputs/train.jsonl", "source_input_line": lines[task_id],
            "input_sha256": input_hash, "input_hash_format": "canonical JSON of all six source input fields",
            "receipt_requirements_file": "data/collection/evaluator_receipt_requirements.jsonl",
            "receipt_requirements_key": task_id,
            "live_tool_schemas_status": "NOT_CAPTURED", "token_count": None,
            "recorded_trace_path": None, "verified_receipt_path": None,
        })
        receipt_rows.append({
            "task_id": task_id, "domain": source["domain"], "role": "train",
            "audience": "EXECUTOR_AND_REVIEWER_ONLY_NEVER_MODEL_INPUT",
            "status": "NOT_COLLECTED", "input_sha256": input_hash,
            "contract_source_file": "data/evaluator_only/train.jsonl",
            **contracts[task_id],
            "required_verifier_indices": list(range(contracts[task_id]["required_checks_total"])),
            "hash_format": "SHA256 of canonical complete verifiers LIST; no wrapper; sorted keys; compact separators; UTF8 ensure_ascii=False; no NaN",
            "receipt_schema": "config/verifier_receipt.schema.json",
            "observed_checks_passed": None, "model_visible_sha256": None,
            "verifier_revision": None, "receipt_path": None,
        })
    domain_plans = []
    for domain in sorted(DOMAIN_HINTS):
        ids = sorted(task for task, source in inputs.items() if source["domain"] == domain)
        tool_counts = Counter(tool for task in ids for tool in inputs[task]["selected_tools"])
        domain_plans.append({
            "domain": domain, "task_count": len(ids),
            "workflow_group_count": len({task_to_group[task] for task in ids}),
            "required_verifier_count": sum(contracts[task]["required_checks_total"] for task in ids),
            "status_counts": {"NOT_COLLECTED": len(ids)},
            "task_ids": ids, "declared_unique_tool_count": len(tool_counts),
            "declared_tool_task_counts": dict(sorted(tool_counts.items())),
            "collection_hints": DOMAIN_HINTS[domain],
            "live_tool_schema_availability": "NOT_CHECKED_BY_QUEUE_BUILDER",
            "backend_execution_readiness": "NOT_CHECKED_BY_QUEUE_BUILDER",
            "observed_input_tokens": None, "observed_output_tokens": None,
            "observed_total_cost_usd": None,
        })
    files = {
        "task_index.jsonl": "".join(canonical_bytes(row).decode() + "\n" for row in rows),
        "evaluator_receipt_requirements.jsonl": "".join(canonical_bytes(row).decode() + "\n" for row in receipt_rows),
        "domain_collection_plan.json": json.dumps({
            "schema_version": 1, "scope": "TRAINING_ONLY_COLLECTION_PLANNING",
            "audience": "OPERATOR_ONLY; do not send this administrative plan to the teacher",
            "unique_tasks": len(inputs), "unique_workflow_groups": len(set(task_to_group.values())),
            "required_verifier_count": sum(c["required_checks_total"] for c in contracts.values()),
            "sft_ready": False, "verified_demonstrations": 0, "domains": domain_plans,
            "ordering": "One lexicographically first task per audited family, round-robin by domain; then remaining family members, round-robin by domain. No model outcomes or gold solutions used.",
            "limits": ["Audited workflow groups are not a proof of statistical independence.",
                       "Task count and declared tool names do not establish execution readiness or token length.",
                       "No verifier SQL, expected answer/state, environment credentials or seed dumps are embedded in queue files."]
        }, indent=2, sort_keys=True) + "\n",
    }
    manifest = {
        "schema_version": 1, "status": "COLLECTION_PLAN_ONLY",
        "builder_sha256": file_sha256(Path(__file__)),
        "model_calls_made": 0, "environment_runs_performed": 0,
        "collection_status": "NOT_COLLECTED", "verified_demonstrations": 0,
        "task_count": len(inputs), "workflow_group_count": len(set(task_to_group.values())),
        "required_checks_total": sum(c["required_checks_total"] for c in contracts.values()),
        "source_file_sha256": {
            path.relative_to(ROOT).as_posix(): file_sha256(path)
            for path in list(paths.values()) + [split_path, ROOT / "data/metadata/workflow_groups.json",
                                               ROOT / "data/metadata/normalization_manifest.json"]
        },
        "artifact_sha256": {name: hashlib.sha256(content.encode()).hexdigest() for name, content in files.items()},
        "administrative_artifacts_are_model_input": False,
        "training_input_policy": "Fetch exactly the requested training input record by task_id, verify input_sha256, pass only its system/user policies and request plus actual allowlisted MCP tool schemas to the teacher.",
        "progress_policy": "Record actual attempts separately. This deterministic planner refuses to overwrite task-index statuses changed from NOT_COLLECTED.",
    }
    files["collection_manifest.json"] = json.dumps(manifest, indent=2, sort_keys=True) + "\n"
    return files, manifest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Verify existing deterministic artifacts; write nothing")
    args = parser.parse_args()
    try:
        files, manifest = build_artifacts()
        destination = ROOT / "data/collection"
        if args.check:
            mismatches = [name for name, content in files.items()
                          if not (destination / name).is_file() or (destination / name).read_text() != content]
            if mismatches:
                raise QueueError("Collection artifacts missing/changed: " + ", ".join(mismatches))
        else:
            index_path = destination / "task_index.jsonl"
            if index_path.exists():
                for _, row in read_jsonl(index_path):
                    if row.get("status") != "NOT_COLLECTED" or row.get("recorded_trace_path") or row.get("verified_receipt_path"):
                        raise QueueError("Collection progress exists; do not reset it by rebuilding the plan")
            destination.mkdir(parents=True, exist_ok=True)
            for name, content in files.items():
                path = destination / name
                if not path.exists() or path.read_text() != content:
                    temporary = path.with_suffix(path.suffix + ".tmp")
                    temporary.write_text(content)
                    temporary.replace(path)
        print(json.dumps({"mode": "CHECK" if args.check else "BUILD",
                          "tasks": manifest["task_count"], "workflow_groups": manifest["workflow_group_count"],
                          "required_checks": manifest["required_checks_total"],
                          "status": manifest["collection_status"], "sft_ready": False}))
    except (QueueError, OSError, ValueError, KeyError) as error:
        parser.exit(2, f"Collection plan refused: {error}\n")


if __name__ == "__main__":
    main()
