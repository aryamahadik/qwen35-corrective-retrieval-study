#!/usr/bin/env python3
"""Real, training-only EnterpriseOps trace collection helpers and CLI.

The solver-facing surface is deliberately narrow: a generated bundle containing
only the canonical task messages and selected live tool schemas, plus an exact
assistant-envelope ``step`` command. Seed data, database identifiers, context headers and
verifiers stay in an executor-only state file.  Accepted artifacts are emitted
only after every indexed verifier passes and a separate explicit review accepts
the observed workflow.

This module never opens development or final-test payload files.
"""
from __future__ import annotations

import argparse
from contextlib import contextmanager
import copy
from datetime import datetime, timezone
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import time
from typing import Any
from urllib import error as urlerror
from urllib.parse import urlsplit
from urllib import request as urlrequest
import uuid


ROOT = Path(__file__).resolve().parents[1]
TRAIN_INPUTS = ROOT / "data" / "task_inputs" / "train.jsonl"
TRAIN_CONTRACTS = ROOT / "data" / "evaluator_only" / "train.jsonl"
SPLIT_MANIFEST = ROOT / "data" / "metadata" / "split_manifest.json"
LOCAL_ENVIRONMENT = ROOT / "config" / "local_environment.json"
SOURCE_MANIFEST = ROOT / "data" / "environment" / "source_manifest.json"
IMAGE_MANIFEST = ROOT / "data" / "environment" / "image_manifest.json"
ATTEMPTS_ROOT = ROOT / "data" / "collection" / "attempts"
SFT_ROOT = ROOT / "data" / "sft"
RECEIPTS_ROOT = SFT_ROOT / "receipts"
REVIEWED_TRACES = SFT_ROOT / "reviewed_traces.jsonl"
ACCEPTANCE_LOCK = SFT_ROOT / ".acceptance.lock"
UPSTREAM_REVISION = "271f2c357f763376997dfd16807fcde2474ae41b"
VERIFIER_REVISION = f"enterpriseops-gym@{UPSTREAM_REVISION}+indexed-local-v1"
TASK_INPUT_FIELDS = (
    "task_id",
    "domain",
    "system_prompt",
    "user_prompt",
    "selected_tools",
    "restricted_tools",
)
SAFE_NAME = re.compile(r"[A-Za-z_][A-Za-z0-9_.-]*\Z")
SAFE_ATTEMPT_ID = re.compile(r"[A-Za-z0-9_.-]+\Z")
CHAIN_FIELDS = {"event_sequence", "previous_event_sha256", "event_sha256"}
STATE_INTEGRITY_FIELD = "state_integrity_sha256"
RESERVED_CONTEXT_HEADERS = {"x-database-id", "host", "content-length"}
AUTH_HEADER_ALIASES = {
    # Three frozen training configs carry the correct opaque token under a
    # neighboring EnterpriseOps domain's header name.  The trusted executor
    # normalizes the wire header only; the frozen task bundle and token value
    # remain unchanged and the mapping is recorded in privileged evidence.
    "gym-calendar": {"x-hr-user-token": "x-access-token"},
    "sn-hr-internal": {"x-access-token": "x-hr-user-token"},
}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def canonical_json(value: Any) -> str:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    )


def canonical_sha256(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def _redact_executor_metadata(value: Any, secrets: list[str]) -> tuple[Any, int]:
    """Remove exact executor-only identifiers before a result reaches a solver.

    Raw wire responses remain in the privileged hash-chained event log.  This
    projection changes no business field except occurrences of the exact fresh
    database ID or authentication-token value used by the executor.
    """
    ordered = sorted({item for item in secrets if isinstance(item, str) and len(item) >= 8}, key=len, reverse=True)
    if isinstance(value, str):
        rendered = value
        count = 0
        for secret in ordered:
            occurrences = rendered.count(secret)
            if occurrences:
                rendered = rendered.replace(secret, "[REDACTED_EXECUTOR_METADATA]")
                count += occurrences
        return rendered, count
    if isinstance(value, list):
        output = []
        count = 0
        for child in value:
            cleaned, child_count = _redact_executor_metadata(child, ordered)
            output.append(cleaned)
            count += child_count
        return output, count
    if isinstance(value, dict):
        output: dict[str, Any] = {}
        count = 0
        for key, child in value.items():
            clean_key, key_count = _redact_executor_metadata(str(key), ordered)
            cleaned, child_count = _redact_executor_metadata(child, ordered)
            output[clean_key] = cleaned
            count += key_count + child_count
        return output, count
    return copy.deepcopy(value), 0


def sha256_file(path: Path | str) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def strict_json_loads(text: str) -> Any:
    """Load JSON while rejecting duplicate keys and non-JSON numeric constants."""

    def unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        value: dict[str, Any] = {}
        for key, child in pairs:
            if key in value:
                raise ValueError(f"Duplicate JSON object key: {key}")
            value[key] = child
        return value

    def invalid_constant(value: str) -> None:
        raise ValueError(f"Invalid JSON numeric constant: {value}")

    return json.loads(
        text,
        object_pairs_hook=unique_object,
        parse_constant=invalid_constant,
    )


def _state_digest(state: dict[str, Any]) -> str:
    payload = {key: value for key, value in state.items() if key != STATE_INTEGRITY_FIELD}
    return canonical_sha256(payload)


def _write_state(path: Path, state: dict[str, Any]) -> None:
    """Persist an unkeyed integrity envelope.

    This detects accidental/partial mutation only.  It deliberately is not called a
    signature because solver and executor share one OS account in this workflow.
    """
    revision = state.get("state_revision", 0)
    if isinstance(revision, bool) or not isinstance(revision, int) or revision < 0:
        raise ValueError("Invalid attempt state revision")
    state["state_revision"] = revision + 1
    state[STATE_INTEGRITY_FIELD] = _state_digest(state)
    _atomic_json(path, state)


def _validate_state_integrity(state: Any) -> dict[str, Any]:
    if not isinstance(state, dict):
        raise ValueError("Attempt state must be a JSON object")
    supplied = state.get(STATE_INTEGRITY_FIELD)
    if not isinstance(supplied, str) or supplied != _state_digest(state):
        raise ValueError("Attempt state integrity hash mismatch")
    return state


@contextmanager
def _exclusive_lock(path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor = os.open(path, os.O_RDWR | os.O_CREAT, 0o600)
    try:
        fcntl.flock(descriptor, fcntl.LOCK_EX)
        yield
    finally:
        fcntl.flock(descriptor, fcntl.LOCK_UN)
        os.close(descriptor)


def extract_sql_value(payload: Any) -> Any:
    """Match the pinned upstream verifier's observed-result extraction."""
    if not isinstance(payload, dict):
        return payload
    if "data" in payload:
        rows = payload["data"]
    elif "rows" in payload:
        rows = payload["rows"]
    elif "result" in payload:
        return payload["result"]
    else:
        return payload
    if not isinstance(rows, list) or not rows:
        return rows
    if len(rows) == 1:
        row = rows[0]
        if isinstance(row, dict) and len(row) == 1:
            return next(iter(row.values()))
        if isinstance(row, list) and len(row) == 1:
            return row[0]
        return row
    return rows


def compare_values(actual: Any, expected: Any, comparison_type: str) -> bool:
    try:
        if comparison_type == "equals":
            return actual == expected
        if comparison_type == "greater_than":
            return actual > expected
        if comparison_type == "less_than":
            return actual < expected
        if comparison_type == "contains":
            return expected in str(actual)
    except (TypeError, ValueError):
        return False
    return False


def _tool_name(schema: dict[str, Any]) -> str:
    try:
        name = schema["function"]["name"]
    except (KeyError, TypeError):
        raise ValueError("Malformed visible tool schema") from None
    if not isinstance(name, str) or not SAFE_NAME.fullmatch(name):
        raise ValueError("Unsafe or missing visible tool name")
    return name


def validate_solver_response(
    response: Any,
    visible_tools: list[dict[str, Any]],
    pending_call_ids: tuple[str, ...] | list[str] = (),
    *,
    selected_tool_names: list[str] | None = None,
) -> dict[str, Any]:
    if not isinstance(response, dict) or response.get("role") != "assistant":
        raise ValueError("Solver response must be one assistant message object")
    if set(response) - {"role", "content", "reasoning_content", "tool_calls", "usage"}:
        raise ValueError("Solver response contains unsupported fields")
    tools = [_tool_name(tool) for tool in visible_tools]
    if len(tools) != len(set(tools)):
        raise ValueError("Duplicate visible tool schemas")
    expected = list(selected_tool_names) if selected_tool_names is not None else tools
    if len(expected) != len(set(expected)) or set(tools) != set(expected):
        raise ValueError("Live visible tool set differs from selected tools")
    content = response.get("content", "")
    if not isinstance(content, str):
        raise ValueError("Assistant content must be text")
    reasoning = response.get("reasoning_content", "")
    if not isinstance(reasoning, str):
        raise ValueError("Assistant reasoning_content must be text")
    usage = response.get("usage")
    if usage is not None and not isinstance(usage, dict):
        raise ValueError("Assistant usage must be an object or null")
    calls = response.get("tool_calls", [])
    if not isinstance(calls, list):
        raise ValueError("tool_calls must be a list")
    seen = set(pending_call_ids)
    for call in calls:
        if (
            not isinstance(call, dict)
            or call.get("type") != "function"
            or set(call) != {"id", "type", "function"}
        ):
            raise ValueError("Malformed solver tool call")
        call_id = call.get("id")
        function = call.get("function")
        if not isinstance(call_id, str) or not call_id or call_id in seen:
            raise ValueError("Duplicate or empty tool call id")
        if not isinstance(function, dict) or set(function) != {"name", "arguments"}:
            raise ValueError("Malformed solver tool-call function")
        arguments = function["arguments"]
        if function["name"] not in set(expected) or not isinstance(arguments, dict):
            raise ValueError("Unselected tool or invalid arguments")
        if any(not isinstance(key, str) or not SAFE_NAME.fullmatch(key) for key in arguments):
            raise ValueError("Tool argument names must be safe identifiers")
        seen.add(call_id)
    if not calls and not content.strip():
        raise ValueError("Assistant response has neither a tool call nor a final answer")
    return response


class AppendOnlyAttemptLog:
    """A locally hash-chained JSONL log.

    The chain detects accidental edits and makes a final digest bindable, but it is
    not an external signature or an OS boundary.
    """

    def __init__(self, attempt_dir: Path | str, *, create: bool):
        self.directory = Path(attempt_dir)
        self.path = self.directory / "events.jsonl"
        if create:
            self.directory.mkdir(parents=True, exist_ok=False, mode=0o700)
            os.chmod(self.directory, 0o700)
            flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
            if hasattr(os, "O_NOFOLLOW"):
                flags |= os.O_NOFOLLOW
            descriptor = os.open(self.path, flags, 0o600)
            os.close(descriptor)
        elif not self.path.is_file():
            raise FileNotFoundError(self.path)

    def append(self, event: dict[str, Any]) -> None:
        if not isinstance(event, dict):
            raise TypeError("Attempt events must be JSON objects")
        if CHAIN_FIELDS & set(event):
            raise ValueError("Attempt event may not provide hash-chain fields")
        flags = os.O_RDWR | os.O_APPEND
        if hasattr(os, "O_NOFOLLOW"):
            flags |= os.O_NOFOLLOW
        descriptor = os.open(self.path, flags)
        with os.fdopen(descriptor, "r+", encoding="utf-8") as handle:
            fcntl.flock(handle.fileno(), fcntl.LOCK_EX)
            handle.seek(0)
            rows = self._parse_and_validate(handle.read())
            previous = rows[-1]["event_sha256"] if rows else None
            chained = copy.deepcopy(event)
            chained["event_sequence"] = len(rows)
            chained["previous_event_sha256"] = previous
            chained["event_sha256"] = canonical_sha256(chained)
            handle.seek(0, os.SEEK_END)
            handle.write(canonical_json(chained) + "\n")
            handle.flush()
            os.fsync(handle.fileno())

    @staticmethod
    def _parse_and_validate(text: str) -> list[dict[str, Any]]:
        rows: list[dict[str, Any]] = []
        previous = None
        for number, line in enumerate(text.splitlines(), 1):
            if not line.strip():
                continue
            row = strict_json_loads(line)
            if not isinstance(row, dict):
                raise ValueError(f"Non-object attempt event at line {number}")
            if row.get("event_sequence") != len(rows):
                raise ValueError(f"Attempt event sequence mismatch at line {number}")
            if row.get("previous_event_sha256") != previous:
                raise ValueError(f"Attempt event chain mismatch at line {number}")
            supplied = row.get("event_sha256")
            material = {key: value for key, value in row.items() if key != "event_sha256"}
            if not isinstance(supplied, str) or supplied != canonical_sha256(material):
                raise ValueError(f"Attempt event digest mismatch at line {number}")
            previous = supplied
            rows.append(row)
        return rows

    def read(self) -> list[dict[str, Any]]:
        with self.path.open(encoding="utf-8") as handle:
            return self._parse_and_validate(handle.read())

    @property
    def head_sha256(self) -> str | None:
        rows = self.read()
        return rows[-1]["event_sha256"] if rows else None


def review_acceptance_ready(
    review: Any, outcomes: Any, required_count: int
) -> bool:
    if not isinstance(review, dict) or review.get("status") != "accepted":
        return False
    if review.get("no_evaluation_or_privileged_content") is not True:
        return False
    if not isinstance(review.get("reviewer"), str) or not review["reviewer"].strip():
        return False
    if not isinstance(review.get("reviewed_at"), str) or not review["reviewed_at"].strip():
        return False
    if not isinstance(required_count, int) or isinstance(required_count, bool) or required_count <= 0:
        return False
    if not isinstance(outcomes, list) or len(outcomes) != required_count:
        return False
    seen: set[int] = set()
    for outcome in outcomes:
        if not isinstance(outcome, dict):
            return False
        index = outcome.get("verifier_index")
        if type(index) is not int or not 0 <= index < required_count or index in seen:
            return False
        if outcome.get("passed") is not True or outcome.get("error") not in (None, ""):
            return False
        if not isinstance(outcome.get("verifier_name"), str) or not outcome["verifier_name"]:
            return False
        seen.add(index)
    return seen == set(range(required_count))


def build_receipt(
    task_bundle: dict[str, Any],
    attempt: dict[str, Any],
    outcomes: list[dict[str, Any]],
    review: dict[str, Any],
) -> dict[str, Any]:
    verifiers = task_bundle.get("verifiers", [])
    if task_bundle.get("task_input_sha256") != canonical_sha256(task_bundle.get("task_input")):
        raise ValueError("Task-input hash is not bound to the supplied canonical input")
    if task_bundle.get("verifier_contract_sha256") != canonical_sha256(verifiers):
        raise ValueError("Verifier hash is not bound to the supplied verifier list")
    if attempt.get("source_task_id") != task_bundle.get("task_input", {}).get("task_id"):
        raise ValueError("Attempt task identity differs from the canonical task")
    if attempt.get("status") != "RECORDED_PENDING_REVIEW":
        raise ValueError("Attempt is not ready for review")
    if attempt.get("cleanup_success") is not True:
        raise ValueError("Attempt databases were not confirmed cleaned up")
    evidence = attempt.get("execution_evidence")
    if not isinstance(evidence, dict) or not isinstance(evidence.get("event_log_head_sha256"), str):
        raise ValueError("Attempt lacks bound execution evidence")
    if not review_acceptance_ready(review, outcomes, len(verifiers)):
        raise ValueError("Explicit accepted review and all indexed passes are required")
    expected_names = [verifier.get("name") for verifier in verifiers]
    for outcome in outcomes:
        if outcome["verifier_name"] != expected_names[outcome["verifier_index"]]:
            raise ValueError("Verifier outcome name/index mismatch")
    payload = {"messages": attempt["messages"], "tools": attempt["tools"]}
    return {
        "schema_version": 2,
        "source_task_id": attempt["source_task_id"],
        "status": "passed",
        "checks_total": len(verifiers),
        "checks_passed": len(verifiers),
        "model_visible_sha256": canonical_sha256(payload),
        "task_input_sha256": task_bundle["task_input_sha256"],
        "verifier_contract_sha256": task_bundle["verifier_contract_sha256"],
        "verifier_revision": task_bundle["verifier_revision"],
        "outcomes": copy.deepcopy(outcomes),
        "execution_evidence": copy.deepcopy(evidence),
    }


def build_reviewed_trace(
    task_bundle: dict[str, Any],
    attempt: dict[str, Any],
    receipt_ref: dict[str, str],
    review: dict[str, Any],
) -> dict[str, Any]:
    if task_bundle.get("task_input_sha256") != canonical_sha256(task_bundle.get("task_input")):
        raise ValueError("Task-input hash is not bound to the supplied canonical input")
    if task_bundle.get("verifier_contract_sha256") != canonical_sha256(task_bundle.get("verifiers")):
        raise ValueError("Verifier hash is not bound to the supplied verifier list")
    if attempt.get("source_task_id") != task_bundle.get("task_input", {}).get("task_id"):
        raise ValueError("Attempt task identity differs from the canonical task")
    if review.get("status") != "accepted" or review.get("no_evaluation_or_privileged_content") is not True:
        raise ValueError("Accepted independent review is required")
    if attempt.get("status") != "RECORDED_PENDING_REVIEW":
        raise ValueError("Attempt is not ready for accepted-trace construction")
    if attempt.get("cleanup_success") is not True:
        raise ValueError("Attempt cleanup is not complete")
    payload = {"messages": attempt["messages"], "tools": attempt["tools"]}
    return {
        "source_task_id": attempt["source_task_id"],
        "messages": copy.deepcopy(attempt["messages"]),
        "tools": copy.deepcopy(attempt["tools"]),
        "review": {
            "status": "accepted",
            "reviewer": review["reviewer"],
            "reviewed_at": review["reviewed_at"],
            "no_evaluation_or_privileged_content": True,
            "model_visible_sha256": canonical_sha256(payload),
            "task_input_sha256": task_bundle["task_input_sha256"],
            "verifier_receipt": copy.deepcopy(receipt_ref),
        },
        "provenance": copy.deepcopy(attempt["provenance"]),
    }


class LocalCollectionHarness:
    """Dependency-injected collection core used by tests and adapters."""

    def __init__(
        self,
        task_bundle: dict[str, Any],
        solver: Any,
        runtime: Any,
        log: AppendOnlyAttemptLog,
        *,
        teacher_model: str,
        max_iterations: int = 50,
    ):
        self.bundle = task_bundle
        self.solver = solver
        self.runtime = runtime
        self.log = log
        self.teacher_model = teacher_model
        self.max_iterations = max_iterations

    def run_attempt(self) -> dict[str, Any]:
        attempt_id = f"attempt-{uuid.uuid4().hex}"
        task = self.bundle["task_input"]
        messages = [
            {"role": "system", "content": task["system_prompt"]},
            {"role": "user", "content": task["user_prompt"]},
        ]
        tools: list[dict[str, Any]] = []
        outcomes: list[dict[str, Any]] = []
        usage = None
        status = "ATTEMPT_FAILED"
        cleanup_ok = True
        catalog_valid = False
        seen_call_ids: set[str] = set()
        self.log.append(
            {
                "event_type": "attempt_started",
                "attempt_id": attempt_id,
                "source_task_id": task["task_id"],
                "created_at": utc_now(),
            }
        )
        try:
            databases = self.runtime.seed_all(attempt_id)
            self.log.append(
                {
                    "event_type": "databases_seeded",
                    "database_ids": databases,
                    "observed_at": utc_now(),
                }
            )
            tools, routing, catalog_hash, _catalog_record = self.runtime.discover_selected_tools(
                task["selected_tools"]
            )
            validate_solver_response(
                {"role": "assistant", "content": "catalog-validation"},
                tools,
                selected_tool_names=task["selected_tools"],
            )
            catalog_valid = True
            self.log.append(
                {
                    "event_type": "tool_catalog_captured",
                    "catalog_sha256": catalog_hash,
                    "tool_names": [_tool_name(tool) for tool in tools],
                    "routing": routing,
                    "observed_at": utc_now(),
                }
            )
            for _ in range(self.max_iterations):
                response = self.solver.invoke(copy.deepcopy(messages), copy.deepcopy(tools))
                validate_solver_response(
                    response,
                    tools,
                    pending_call_ids=tuple(seen_call_ids),
                    selected_tool_names=task["selected_tools"],
                )
                usage = response.get("usage")
                clean = {key: copy.deepcopy(value) for key, value in response.items() if key in {"role", "content", "reasoning_content", "tool_calls"}}
                clean.setdefault("content", "")
                self.log.append(
                    {
                        "event_type": "assistant_message",
                        "message": clean,
                        "usage": usage,
                        "observed_at": utc_now(),
                    }
                )
                messages.append(clean)
                calls = clean.get("tool_calls", [])
                if not calls:
                    break
                for call in calls:
                    seen_call_ids.add(call["id"])
                    name = call["function"]["name"]
                    arguments = call["function"]["arguments"]
                    self.log.append(
                        {
                            "event_type": "tool_call",
                            "tool_call_id": call["id"],
                            "tool_name": name,
                            "arguments": copy.deepcopy(arguments),
                            "observed_at": utc_now(),
                        }
                    )
                    execution = self.runtime.call_tool(name, arguments)
                    if not isinstance(execution, dict) or "result" not in execution:
                        raise RuntimeError("Runtime returned a malformed tool execution")
                    result = execution["result"]
                    tool_error = isinstance(result, dict) and result.get("isError") is True
                    self.log.append(
                        {
                            "event_type": "tool_result",
                            "tool_call_id": call["id"],
                            "tool_name": name,
                            "result": copy.deepcopy(result),
                            "success": not tool_error,
                            "transport": copy.deepcopy(execution.get("transport")),
                            "observed_at": utc_now(),
                        }
                    )
                    messages.append(
                        {
                            "role": "tool",
                            "tool_call_id": call["id"],
                            "name": name,
                            "content": canonical_json(result),
                        }
                    )
            else:
                raise RuntimeError("Solver exceeded maximum iterations")
            if messages[-1].get("role") != "assistant" or messages[-1].get("tool_calls"):
                raise RuntimeError("Solver did not return a final assistant answer")
            for index, verifier in enumerate(self.bundle["verifiers"]):
                config = verifier.get("validation_config", {})
                try:
                    execution = self.runtime.run_sql(verifier.get("gym_name"), config["query"])
                    if not isinstance(execution, dict) or "result" not in execution:
                        raise RuntimeError("Runtime returned a malformed SQL execution")
                    actual = extract_sql_value(execution["result"])
                    passed = compare_values(
                        actual,
                        config.get("expected_value"),
                        config.get("comparison_type", "equals"),
                    )
                    outcome = {
                        "verifier_index": index,
                        "verifier_name": verifier["name"],
                        "passed": bool(passed),
                        "error": None,
                    }
                except Exception as exc:
                    outcome = {
                        "verifier_index": index,
                        "verifier_name": verifier["name"],
                        "passed": False,
                        "error": str(exc),
                    }
                outcomes.append(outcome)
                self.log.append({"event_type": "verifier_outcome", **outcome, "observed_at": utc_now()})
            status = (
                "RECORDED_PENDING_REVIEW"
                if all(item["passed"] and item["error"] in (None, "") for item in outcomes)
                else "ATTEMPT_FAILED"
            )
        except Exception as exc:
            status = "BLOCKED_BACKEND" if not catalog_valid else "ATTEMPT_FAILED"
            self.log.append(
                {
                    "event_type": "attempt_error",
                    "error": str(exc),
                    "observed_at": utc_now(),
                }
            )
        finally:
            try:
                self.runtime.cleanup()
                self.log.append({"event_type": "cleanup", "success": True, "error": None, "observed_at": utc_now()})
            except Exception as exc:
                cleanup_ok = False
                status = "ATTEMPT_FAILED"
                self.log.append({"event_type": "cleanup", "success": False, "error": str(exc), "observed_at": utc_now()})
        summary = {
            "attempt_id": attempt_id,
            "source_task_id": task["task_id"],
            "status": status,
            "messages": messages,
            "tools": tools,
            "outcomes": outcomes,
            "usage": usage,
            "cleanup_success": cleanup_ok,
            "provenance": {
                "teacher_model": self.teacher_model,
                "generator_revision": self.bundle["generator_revision"],
                "environment_revision": self.bundle["environment_revision"],
                "source_trace_id": attempt_id,
            },
        }
        self.log.append(
            {
                "event_type": "attempt_finished",
                "status": status,
                "finished_at": utc_now(),
            }
        )
        return summary


def _load_jsonl_by_id(path: Path, task_id: str) -> dict[str, Any]:
    found = None
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            if not line.strip():
                continue
            row = strict_json_loads(line)
            if not isinstance(row, dict):
                raise ValueError(f"Non-object JSONL row in {path.name}")
            if row.get("task_id") == task_id:
                if found is not None:
                    raise ValueError(f"Duplicate task ID in {path.name}: {task_id}")
                found = row
    if found is None:
        raise KeyError(f"Training task not found: {task_id}")
    return found


def _verified_seed_evidence(
    gym_configs: list[dict[str, Any]], source: dict[str, Any]
) -> list[dict[str, Any]]:
    if source.get("revision") != UPSTREAM_REVISION:
        raise ValueError("Source manifest revision differs from the pinned upstream revision")
    entries = source.get("training_seed_files")
    if not isinstance(entries, list):
        raise ValueError("Source manifest lacks the training seed inventory")
    by_local_path: dict[str, dict[str, Any]] = {}
    for entry in entries:
        if not isinstance(entry, dict) or not isinstance(entry.get("local_path"), str):
            raise ValueError("Malformed training seed manifest entry")
        if entry["local_path"] in by_local_path:
            raise ValueError("Duplicate training seed manifest path")
        by_local_path[entry["local_path"]] = entry
    evidence: list[dict[str, Any]] = []
    seed_root = (ROOT / "data" / "environment" / "seed_sql").resolve()
    for config in gym_configs:
        relative = Path(config["seed_database_file"])
        path = (seed_root / relative).resolve()
        if not path.is_relative_to(seed_root) or not path.is_file():
            raise FileNotFoundError(f"Pinned training seed missing: {relative}")
        local_path = path.relative_to(ROOT).as_posix()
        expected = by_local_path.get(local_path)
        if not expected:
            raise ValueError(f"Training seed is absent from source manifest: {local_path}")
        actual_size = path.stat().st_size
        actual_sha = sha256_file(path)
        if expected.get("bytes") != actual_size or expected.get("sha256") != actual_sha:
            raise ValueError(f"Training seed integrity mismatch: {local_path}")
        evidence.append(
            {
                "gym_name": config["mcp_server_name"],
                "local_path": local_path,
                "bytes": actual_size,
                "sha256": actual_sha,
            }
        )
    return evidence


def load_task_bundle(task_id: str) -> dict[str, Any]:
    split = strict_json_loads(SPLIT_MANIFEST.read_text(encoding="utf-8"))
    train_ids = set(split["task_ids"]["train"])
    if task_id not in train_ids:
        raise ValueError("Only frozen training task IDs may be collected")
    public = _load_jsonl_by_id(TRAIN_INPUTS, task_id)
    contract = _load_jsonl_by_id(TRAIN_CONTRACTS, task_id)
    task_input = {field: public[field] for field in TASK_INPUT_FIELDS}
    if {field: contract[field] for field in TASK_INPUT_FIELDS} != task_input:
        raise ValueError("Canonical training input differs from evaluator contract")
    verifiers = contract.get("verifiers")
    if not isinstance(verifiers, list) or not verifiers:
        raise ValueError("Training task has no verifier contract")
    names = [item.get("name") for item in verifiers]
    if any(not isinstance(name, str) or not name for name in names) or len(names) != len(set(names)):
        raise ValueError("Verifier names must be nonempty and unique")
    gym_configs = contract.get("gym_servers_config")
    if not isinstance(gym_configs, list) or not gym_configs:
        raise ValueError("Training task has no gym server configuration")
    gym_names = [row.get("mcp_server_name") for row in gym_configs if isinstance(row, dict)]
    if len(gym_names) != len(gym_configs) or len(gym_names) != len(set(gym_names)):
        raise ValueError("Gym server names must be present and unique")
    environment = strict_json_loads(LOCAL_ENVIRONMENT.read_text(encoding="utf-8"))
    source = strict_json_loads(SOURCE_MANIFEST.read_text(encoding="utf-8"))
    seed_evidence = _verified_seed_evidence(gym_configs, source)
    if not IMAGE_MANIFEST.is_file():
        raise FileNotFoundError("Pinned image manifest is missing")
    server_images: dict[str, str] = {}
    for name in gym_names:
        spec = environment.get("servers", {}).get(name)
        if not isinstance(spec, dict) or not isinstance(spec.get("image"), str):
            raise ValueError(f"Local environment lacks a pinned image for {name}")
        server_images[name] = spec["image"]
    revision_material = {
        "upstream_revision": source.get("revision"),
        "source_manifest_sha256": sha256_file(SOURCE_MANIFEST),
        "image_manifest_sha256": sha256_file(IMAGE_MANIFEST),
        "servers": dict(sorted(server_images.items())),
        "training_seeds": seed_evidence,
    }
    return {
        "task_input": task_input,
        "verifiers": verifiers,
        "gym_servers_config": gym_configs,
        "mcp_endpoint": contract.get("mcp_endpoint", "/mcp"),
        "task_input_sha256": canonical_sha256(task_input),
        "verifier_contract_sha256": canonical_sha256(verifiers),
        "generator_revision": sha256_file(Path(__file__)),
        "environment_revision": canonical_sha256(revision_material),
        "verifier_revision": VERIFIER_REVISION,
        "environment_contract": revision_material,
    }


def _normal_header(key: str) -> str:
    normalized = key.lower().replace("_", "-")
    return normalized if normalized.startswith("x-") else f"x-{normalized}"


class _RejectRedirects(urlrequest.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise RuntimeError(f"HTTP redirect is not permitted: {code} {newurl}")


def _http_json(
    url: str,
    *,
    method: str = "GET",
    payload: dict[str, Any] | None = None,
    headers: dict[str, str] | None = None,
    timeout: float = 120.0,
    allow_empty: bool = False,
) -> tuple[int, str, Any, dict[str, str]]:
    body = None if payload is None else canonical_json(payload).encode("utf-8")
    final_headers = {"Accept": "application/json"}
    if payload is not None:
        final_headers["Content-Type"] = "application/json"
    if headers:
        final_headers.update(headers)
    req = urlrequest.Request(url, data=body, headers=final_headers, method=method)
    try:
        opener = urlrequest.build_opener(urlrequest.ProxyHandler({}), _RejectRedirects())
        with opener.open(req, timeout=timeout) as response:
            raw_bytes = response.read(32 * 1024 * 1024 + 1)
            if len(raw_bytes) > 32 * 1024 * 1024:
                raise RuntimeError(f"Oversized HTTP response from {url}")
            raw = raw_bytes.decode("utf-8")
            status = response.status
            response_headers = {key.lower(): value for key, value in response.headers.items()}
    except urlerror.HTTPError as exc:
        raw = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"HTTP {exc.code} from {url}: {raw}") from exc
    except UnicodeDecodeError as exc:
        raise RuntimeError(f"Non-UTF8 response from {url}") from exc
    if not 200 <= status < 300:
        raise RuntimeError(f"Unexpected HTTP {status} from {url}")
    if not raw:
        if allow_empty:
            return status, raw, None, response_headers
        raise RuntimeError(f"Empty JSON response from {url}")
    content_type = response_headers.get("content-type", "").split(";", 1)[0].strip().lower()
    if content_type not in {"application/json", "application/json-rpc"}:
        raise RuntimeError(f"Unexpected JSON content type from {url}: {content_type or 'missing'}")
    try:
        parsed = strict_json_loads(raw)
    except (TypeError, ValueError) as exc:
        raise RuntimeError(f"Invalid JSON response from {url}") from exc
    return status, raw, parsed, response_headers


class CleanupError(RuntimeError):
    def __init__(self, message: str, results: list[dict[str, Any]]):
        super().__init__(message)
        self.results = results


class HTTPTaskRuntime:
    """Executor-only adapter for attested loopback benchmark services."""

    def __init__(
        self,
        bundle: dict[str, Any],
        *,
        attempt_id: str,
        databases: dict[str, str] | None = None,
        routing: dict[str, str] | None = None,
        session_ids: dict[str, str] | None = None,
    ):
        self.bundle = bundle
        self.attempt_id = attempt_id
        self.databases = dict(databases or {})
        self.routing = dict(routing or {})
        self.session_ids = dict(session_ids or {})
        self.environment = strict_json_loads(LOCAL_ENVIRONMENT.read_text(encoding="utf-8"))
        rows = bundle.get("gym_servers_config")
        if not isinstance(rows, list) or not rows:
            raise ValueError("Runtime requires a nonempty gym configuration")
        self.configs = {row["mcp_server_name"]: copy.deepcopy(row) for row in rows}
        if len(self.configs) != len(rows):
            raise ValueError("Runtime gym names must be unique")
        self.context_header_normalizations: dict[str, list[dict[str, str]]] = {}

    def _base(self, gym_name: str) -> str:
        configured = self.environment.get("servers", {}).get(gym_name)
        if not isinstance(configured, dict):
            raise ValueError(f"Unconfigured local training server: {gym_name}")
        url = configured.get("url")
        if not isinstance(url, str):
            raise ValueError(f"Missing local URL for {gym_name}")
        parsed = urlsplit(url)
        try:
            port = parsed.port
        except ValueError as exc:
            raise ValueError(f"Invalid local port for {gym_name}") from exc
        if (
            parsed.scheme != "http"
            or parsed.hostname not in {"localhost", "127.0.0.1", "::1"}
            or port is None
            or parsed.username is not None
            or parsed.password is not None
            or parsed.query
            or parsed.fragment
            or parsed.path not in {"", "/"}
        ):
            raise ValueError("Only explicit loopback HTTP benchmark origins are permitted")
        return url.rstrip("/")

    def _headers(self, gym_name: str, *, include_database: bool = True) -> dict[str, str]:
        headers: dict[str, str] = {}
        context = self.configs[gym_name].get("context") or {}
        if not isinstance(context, dict):
            raise ValueError(f"Malformed context for {gym_name}")
        for key, value in context.items():
            header = _normal_header(str(key))
            if header in RESERVED_CONTEXT_HEADERS or "\n" in header or "\r" in header:
                raise ValueError(f"Context attempts to override a reserved header: {key}")
            rendered = str(value)
            if "\n" in rendered or "\r" in rendered:
                raise ValueError(f"Unsafe context header value: {key}")
            headers[header] = rendered
        normalizations: list[dict[str, str]] = []
        for source, target in AUTH_HEADER_ALIASES.get(gym_name, {}).items():
            if source not in headers:
                continue
            if target in headers:
                raise ValueError(
                    f"Ambiguous authentication context for {gym_name}: both {source} and {target}"
                )
            headers[target] = headers.pop(source)
            normalizations.append({"source_header": source, "target_header": target})
        if normalizations:
            self.context_header_normalizations[gym_name] = normalizations
        if include_database:
            headers["x-database-id"] = self.databases[gym_name]
        session_id = self.session_ids.get(gym_name)
        if session_id:
            headers["mcp-session-id"] = session_id
        return headers

    def model_visible_result(self, value: Any) -> tuple[Any, dict[str, Any]]:
        secrets = list(self.databases.values())
        for config in self.configs.values():
            for key, raw_value in (config.get("context") or {}).items():
                normalized = _normal_header(str(key))
                if "token" in normalized or "authorization" in normalized or "api-key" in normalized:
                    secrets.append(str(raw_value))
        cleaned, count = _redact_executor_metadata(value, secrets)
        return cleaned, {
            "policy": "exact_executor_database_and_auth_token_redaction_v1",
            "replacement_count": count,
            "raw_response_preserved_in_privileged_event_log": True,
        }

    @staticmethod
    def _docker_json(arguments: list[str]) -> Any:
        try:
            completed = subprocess.run(
                ["docker", *arguments],
                cwd=ROOT,
                capture_output=True,
                text=True,
                timeout=20,
                check=False,
            )
        except (OSError, subprocess.TimeoutExpired) as exc:
            raise RuntimeError("Docker inspection is unavailable") from exc
        if completed.returncode != 0:
            raise RuntimeError(f"Docker inspection failed: {completed.stderr.strip()}")
        return strict_json_loads(completed.stdout)

    def attest_live_environment(self) -> dict[str, Any]:
        """Bind each configured port to one running container with the pinned digest."""
        container_ids = subprocess.run(
            ["docker", "ps", "-q"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            timeout=20,
            check=False,
        )
        if container_ids.returncode != 0:
            raise RuntimeError(f"Docker is unavailable: {container_ids.stderr.strip()}")
        ids = [item for item in container_ids.stdout.splitlines() if item]
        if not ids:
            raise RuntimeError("No running benchmark containers were found")
        inspected = self._docker_json(["inspect", *ids])
        if not isinstance(inspected, list):
            raise RuntimeError("Unexpected Docker container inspection response")
        evidence: dict[str, Any] = {}
        for gym_name in self.configs:
            spec = self.environment["servers"][gym_name]
            parsed = urlsplit(self._base(gym_name))
            host_port = str(parsed.port)
            container_port = f"{spec['container_port']}/tcp"
            matches = []
            for item in inspected:
                if not isinstance(item, dict) or not item.get("State", {}).get("Running"):
                    continue
                bindings = item.get("NetworkSettings", {}).get("Ports", {}).get(container_port) or []
                if any(
                    str(binding.get("HostPort")) == host_port
                    and binding.get("HostIp") in {"127.0.0.1", "::1"}
                    for binding in bindings
                    if isinstance(binding, dict)
                ):
                    matches.append(item)
            if len(matches) != 1:
                raise RuntimeError(
                    f"Expected exactly one loopback-bound container for {gym_name}; found {len(matches)}"
                )
            container = matches[0]
            image_id = container.get("Image")
            image_info = self._docker_json(["image", "inspect", str(image_id)])
            if not isinstance(image_info, list) or len(image_info) != 1:
                raise RuntimeError(f"Could not inspect the live image for {gym_name}")
            repo_digests = image_info[0].get("RepoDigests") or []
            expected_image = spec.get("image")
            if expected_image not in repo_digests and container.get("Config", {}).get("Image") != expected_image:
                raise RuntimeError(f"Live container image differs from the pinned digest for {gym_name}")
            evidence[gym_name] = {
                "container_id": container.get("Id"),
                "image_id": image_id,
                "image": expected_image,
                "host": parsed.hostname,
                "host_port": parsed.port,
                "container_port": spec["container_port"],
            }
        return evidence

    def plan_databases(self) -> dict[str, str]:
        if self.databases:
            raise ValueError("Attempt databases were already planned")
        self.databases = {
            gym_name: f"db_{int(time.time() * 1000)}_{uuid.uuid4().hex[:12]}"
            for gym_name in self.configs
        }
        return dict(self.databases)

    def seed_all(
        self,
        attempt_id: str | None = None,
        *,
        on_seed_start: Any = None,
        on_seed: Any = None,
    ) -> dict[str, str]:
        if attempt_id is not None and attempt_id != self.attempt_id:
            raise ValueError("Runtime attempt ID mismatch")
        if not self.databases:
            self.plan_databases()
        current = _verified_seed_evidence(
            list(self.configs.values()),
            strict_json_loads(SOURCE_MANIFEST.read_text(encoding="utf-8")),
        )
        expected = self.bundle.get("environment_contract", {}).get("training_seeds")
        if current != expected:
            raise ValueError("Training seed evidence changed after task load")
        seed_root = (ROOT / "data" / "environment" / "seed_sql").resolve()
        for gym_name, config in self.configs.items():
            relative = Path(config["seed_database_file"])
            path = (seed_root / relative).resolve()
            database_id = self.databases[gym_name]
            sql_content = path.read_text(encoding="utf-8")
            payload = {
                "database_id": database_id,
                "name": f"training-attempt-{self.attempt_id}",
                "description": f"isolated training attempt from {relative.name}",
                "sql_content": sql_content,
            }
            if on_seed_start:
                on_seed_start(gym_name, database_id)
            status, raw, parsed, _ = _http_json(
                self._base(gym_name) + "/api/seed-database",
                method="POST",
                payload=payload,
                timeout=max(120.0, len(sql_content) / 5000),
            )
            if isinstance(parsed, dict) and parsed.get("success") is False:
                raise RuntimeError(f"Seed endpoint rejected {gym_name}: {parsed.get('error')}")
            detail = {
                "gym_name": gym_name,
                "database_id": database_id,
                "http_status": status,
                "request_sha256": canonical_sha256(payload),
                "response_sha256": hashlib.sha256(raw.encode("utf-8")).hexdigest(),
            }
            if on_seed:
                on_seed(detail)
        return dict(self.databases)

    def _mcp_notification(self, gym_name: str, method: str, params: dict[str, Any]) -> None:
        payload = {"jsonrpc": "2.0", "method": method, "params": params}
        _, _, parsed, _ = _http_json(
            self._base(gym_name) + self.bundle.get("mcp_endpoint", "/mcp"),
            method="POST",
            payload=payload,
            headers=self._headers(gym_name),
            timeout=60.0,
            allow_empty=True,
        )
        # Several pinned EnterpriseOps servers acknowledge notifications even
        # though JSON-RPC notifications normally have no response.  Accept only
        # their exact, content-free acknowledgement and record no inferred data.
        if parsed is not None and parsed != {"jsonrpc": "2.0", "id": None, "result": {}}:
            raise RuntimeError(f"MCP notification returned an invalid acknowledgement for {gym_name}")

    def _mcp(self, gym_name: str, method: str, params: dict[str, Any]) -> dict[str, Any]:
        request_id = f"{self.attempt_id}:{uuid.uuid4().hex}"
        payload = {
            "jsonrpc": "2.0",
            "id": request_id,
            "method": method,
            "params": params,
        }
        status, raw, parsed, response_headers = _http_json(
            self._base(gym_name) + self.bundle.get("mcp_endpoint", "/mcp"),
            method="POST",
            payload=payload,
            headers=self._headers(gym_name),
            timeout=60.0,
        )
        if not isinstance(parsed, dict):
            raise RuntimeError(f"MCP response is not an object for {gym_name}")
        if parsed.get("jsonrpc") != "2.0" or parsed.get("id") != request_id:
            raise RuntimeError(f"MCP response envelope mismatch from {gym_name}")
        has_result = "result" in parsed
        has_error = "error" in parsed
        if has_result == has_error:
            raise RuntimeError(f"MCP response must contain exactly one result or error from {gym_name}")
        session_id = response_headers.get("mcp-session-id")
        if session_id:
            previous = self.session_ids.get(gym_name)
            if previous is not None and previous != session_id:
                raise RuntimeError(f"MCP session changed unexpectedly for {gym_name}")
            self.session_ids[gym_name] = session_id
        transport = {
            "protocol": "jsonrpc-2.0-http",
            "method": method,
            "request_id": request_id,
            "http_status": status,
            "request_sha256": canonical_sha256(payload),
            "response_sha256": hashlib.sha256(raw.encode("utf-8")).hexdigest(),
            "session_id_sha256": (
                hashlib.sha256(session_id.encode("utf-8")).hexdigest() if session_id else None
            ),
            "normalization": "jsonrpc.result serialized as canonical JSON tool content",
        }
        if has_error:
            raise RuntimeError(f"MCP error from {gym_name}: {canonical_json(parsed['error'])}")
        return {"result": parsed["result"], "raw_response": raw, "transport": transport}

    def discover_selected_tools(
        self, selected_names: list[str]
    ) -> tuple[list[dict[str, Any]], dict[str, str], str, dict[str, Any]]:
        selected = set(selected_names)
        found: dict[str, dict[str, Any]] = {}
        routing: dict[str, str] = {}
        raw_catalogs: dict[str, Any] = {}
        transports: dict[str, Any] = {}
        for gym_name in self.configs:
            initialized = self._mcp(
                gym_name,
                "initialize",
                {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {"tools": {}},
                    "clientInfo": {"name": "training-collection-harness", "version": "2.0"},
                },
            )
            self._mcp_notification(gym_name, "notifications/initialized", {})
            listed = self._mcp(gym_name, "tools/list", {})
            result = listed["result"]
            catalog = result.get("tools", []) if isinstance(result, dict) else []
            raw_catalogs[gym_name] = catalog
            transports[gym_name] = {
                "initialize": initialized["transport"],
                "tools_list": listed["transport"],
            }
            for raw_tool in catalog:
                name = raw_tool.get("name") if isinstance(raw_tool, dict) else None
                if name not in selected:
                    continue
                if name in found:
                    raise ValueError(f"Selected tool is ambiguous across live servers: {name}")
                parameters = raw_tool.get("inputSchema")
                if not isinstance(parameters, dict):
                    raise ValueError(f"Selected live tool lacks inputSchema: {name}")
                function: dict[str, Any] = {
                    "name": name,
                    "description": raw_tool.get("description", ""),
                    "parameters": copy.deepcopy(parameters),
                }
                found[name] = {"type": "function", "function": function}
                routing[name] = gym_name
        missing = selected - set(found)
        if missing:
            raise ValueError(f"Selected tools missing from live catalogs: {sorted(missing)}")
        tools = [found[name] for name in selected_names]
        self.routing = routing
        catalog_record = {
            "raw_catalogs": raw_catalogs,
            "selected_tools": tools,
            "routing": routing,
            "transport": transports,
        }
        return tools, routing, canonical_sha256(catalog_record), catalog_record

    def call_tool(self, name: str, arguments: dict[str, Any]) -> dict[str, Any]:
        if name not in self.routing:
            raise ValueError(f"Tool is not selected for this attempt: {name}")
        return self._mcp(
            self.routing[name],
            "tools/call",
            {"name": name, "arguments": arguments},
        )

    def run_sql(self, gym_name: str | None, query: str) -> dict[str, Any]:
        if not gym_name:
            if len(self.configs) != 1:
                raise ValueError("Hybrid verifier is missing gym_name")
            gym_name = next(iter(self.configs))
        if gym_name not in self.configs:
            raise ValueError(f"Verifier names an unavailable gym: {gym_name}")
        payload = {"query": query, "database_id": self.databases[gym_name]}
        status, raw, parsed, _ = _http_json(
            self._base(gym_name) + "/api/sql-runner",
            method="POST",
            payload=payload,
            headers=self._headers(gym_name),
            timeout=60.0,
        )
        if isinstance(parsed, dict) and parsed.get("success") is False:
            raise RuntimeError(f"SQL endpoint reported failure: {parsed.get('error')}")
        return {
            "result": parsed,
            "raw_response": raw,
            "transport": {
                "protocol": "http-json",
                "http_status": status,
                "request_sha256": canonical_sha256(payload),
                "response_sha256": hashlib.sha256(raw.encode("utf-8")).hexdigest(),
            },
        }

    def cleanup(self, *, on_result: Any = None) -> list[dict[str, Any]]:
        results: list[dict[str, Any]] = []
        errors = []
        for gym_name, database_id in list(self.databases.items()):
            try:
                payload = {"database_id": database_id}
                status, raw, parsed, _ = _http_json(
                    self._base(gym_name) + "/api/delete-database",
                    method="DELETE",
                    payload=payload,
                    timeout=60.0,
                )
                if isinstance(parsed, dict) and parsed.get("success") is False:
                    raise RuntimeError(str(parsed.get("error") or "delete endpoint reported failure"))
                detail = {
                    "gym_name": gym_name,
                    "database_id": database_id,
                    "success": True,
                    "http_status": status,
                    "request_sha256": canonical_sha256(payload),
                    "response_sha256": hashlib.sha256(raw.encode("utf-8")).hexdigest(),
                }
            except Exception as exc:
                detail = {
                    "gym_name": gym_name,
                    "database_id": database_id,
                    "success": False,
                    "error": str(exc),
                }
                errors.append(f"{gym_name}: {exc}")
            results.append(detail)
            if on_result:
                on_result(detail)
        if errors:
            raise CleanupError("; ".join(errors), results)
        return results


def _atomic_json(path: Path, value: Any, *, mode: int = 0o600) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary = tempfile.mkstemp(prefix=path.name + ".", dir=path.parent)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
            handle.write(json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + "\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.chmod(temporary, mode)
        os.replace(temporary, path)
        directory_fd = os.open(path.parent, os.O_RDONLY)
        try:
            os.fsync(directory_fd)
        finally:
            os.close(directory_fd)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def _pretty_json_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + "\n").encode("utf-8")


def _exclusive_bytes(path: Path, payload: bytes, *, mode: int = 0o600) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    descriptor = os.open(path, flags, mode)
    try:
        offset = 0
        while offset < len(payload):
            offset += os.write(descriptor, payload[offset:])
        os.fsync(descriptor)
    finally:
        os.close(descriptor)
    directory_fd = os.open(path.parent, os.O_RDONLY)
    try:
        os.fsync(directory_fd)
    finally:
        os.close(directory_fd)


def _append_bytes(path: Path, payload: bytes, *, mode: int = 0o600) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    flags = os.O_WRONLY | os.O_CREAT | os.O_APPEND
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    descriptor = os.open(path, flags, mode)
    try:
        offset = 0
        while offset < len(payload):
            offset += os.write(descriptor, payload[offset:])
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def _attempt_dir(attempt_id: str) -> Path:
    if (
        not isinstance(attempt_id, str)
        or not SAFE_ATTEMPT_ID.fullmatch(attempt_id)
        or attempt_id in {".", ".."}
    ):
        raise ValueError("Unsafe attempt ID")
    matches = list(ATTEMPTS_ROOT.glob(f"*/{attempt_id}"))
    if len(matches) != 1:
        raise FileNotFoundError(f"Expected one attempt directory for {attempt_id}; found {len(matches)}")
    resolved = matches[0].resolve()
    if not resolved.is_relative_to(ATTEMPTS_ROOT.resolve()) or resolved.name != attempt_id:
        raise ValueError("Attempt directory escapes the collection root")
    return resolved


def _contract_view(bundle: dict[str, Any]) -> dict[str, Any]:
    return {
        "task_input": bundle.get("task_input"),
        "verifiers": bundle.get("verifiers"),
        "gym_servers_config": bundle.get("gym_servers_config"),
        "mcp_endpoint": bundle.get("mcp_endpoint"),
        "task_input_sha256": bundle.get("task_input_sha256"),
        "verifier_contract_sha256": bundle.get("verifier_contract_sha256"),
        "verifier_revision": bundle.get("verifier_revision"),
        "environment_revision": bundle.get("environment_revision"),
        "environment_contract": bundle.get("environment_contract"),
        "generator_revision": bundle.get("generator_revision"),
    }


def _validate_transcript_prefix(state: dict[str, Any], fresh: dict[str, Any]) -> None:
    messages = state.get("messages")
    tools = state.get("tools")
    if not isinstance(messages, list) or len(messages) < 2 or not isinstance(tools, list):
        raise ValueError("Attempt state lacks a model-visible transcript")
    task = fresh["task_input"]
    if messages[:2] != [
        {"role": "system", "content": task["system_prompt"]},
        {"role": "user", "content": task["user_prompt"]},
    ]:
        raise ValueError("Attempt transcript does not start with the exact canonical messages")
    if state.get("status") == "INITIALIZING" and not tools and len(messages) == 2:
        return
    names = [_tool_name(tool) for tool in tools]
    if len(names) != len(set(names)) or set(names) != set(task["selected_tools"]):
        raise ValueError("Attempt visible tools differ from the canonical selected-tool set")
    pending: dict[str, str] = {}
    seen: set[str] = set()
    for message in messages[2:]:
        if not isinstance(message, dict) or message.get("role") not in {"assistant", "tool"}:
            raise ValueError("Attempt transcript contains an invalid later role")
        role = message["role"]
        if pending and role != "tool":
            raise ValueError("Attempt transcript has an unanswered tool call")
        if role == "assistant":
            validate_solver_response(message, tools, pending_call_ids=tuple(seen), selected_tool_names=task["selected_tools"])
            for call in message.get("tool_calls", []):
                pending[call["id"]] = call["function"]["name"]
                seen.add(call["id"])
        else:
            if set(message) - {"role", "content", "tool_call_id", "name"}:
                raise ValueError("Attempt tool result contains unsupported fields")
            call_id = message.get("tool_call_id")
            if call_id not in pending:
                raise ValueError("Attempt transcript has an orphan tool result")
            if message.get("name") != pending[call_id]:
                raise ValueError("Attempt tool result name does not match its call")
            if not isinstance(message.get("content"), str) or not message["content"].strip():
                raise ValueError("Attempt tool result must contain text")
            del pending[call_id]
    if pending:
        inflight = state.get("inflight_step")
        inflight_calls = inflight.get("calls") if isinstance(inflight, dict) else None
        allowed_pending = (
            state.get("status") == "IN_PROGRESS"
            and isinstance(inflight_calls, dict)
            and set(pending) == {
                call_id for call_id, status in inflight_calls.items() if status == "pending"
            }
        )
        if not allowed_pending:
            raise ValueError("Attempt transcript ends with an unanswered tool call")
    if state.get("status") in {"RECORDED_PENDING_VERIFICATION", "RECORDED_PENDING_REVIEW", "ACCEPTED"}:
        final = messages[-1]
        if final.get("role") != "assistant" or final.get("tool_calls"):
            raise ValueError("Finished attempt lacks a final assistant response")


def _freshen_and_validate_state(directory: Path, state: dict[str, Any]) -> dict[str, Any]:
    _validate_state_integrity(state)
    task_id = state.get("source_task_id")
    if not isinstance(task_id, str):
        raise ValueError("Attempt state lacks a source task ID")
    if state.get("attempt_id") != directory.name or task_id != directory.parent.name:
        raise ValueError("Attempt state identity differs from its directory")
    if state.get("provenance", {}).get("source_trace_id") != directory.name:
        raise ValueError("Attempt provenance identity mismatch")
    fresh = load_task_bundle(task_id)
    stored = state.get("task_bundle")
    if not isinstance(stored, dict) or _contract_view(stored) != _contract_view(fresh):
        raise ValueError("Attempt contract no longer matches the frozen training files")
    if fresh["task_input_sha256"] != canonical_sha256(fresh["task_input"]):
        raise ValueError("Fresh canonical task-input binding failed")
    if fresh["verifier_contract_sha256"] != canonical_sha256(fresh["verifiers"]):
        raise ValueError("Fresh canonical verifier binding failed")
    catalog_path = directory / "catalog.executor-only.json"
    if state.get("catalog_sha256") is not None:
        if not catalog_path.is_file():
            raise ValueError("Attempt catalog evidence is missing")
        catalog = strict_json_loads(catalog_path.read_text(encoding="utf-8"))
        if canonical_sha256(catalog) != state.get("catalog_sha256"):
            raise ValueError("Attempt catalog evidence hash mismatch")
        if catalog.get("selected_tools") != state.get("tools") or catalog.get("routing") != state.get("routing"):
            raise ValueError("Attempt visible schemas/routing differ from captured live catalog")
        live_environment = state.get("live_environment")
        if not isinstance(live_environment, dict):
            raise ValueError("Attempt lacks live container evidence")
        fresh_runtime = HTTPTaskRuntime(fresh, attempt_id=state["attempt_id"])
        for gym_name in fresh_runtime.configs:
            fresh_runtime._headers(gym_name, include_database=False)
        expected_header_normalizations = fresh_runtime.context_header_normalizations
        if state.get("executor_context_header_normalizations", {}) != expected_header_normalizations:
            raise ValueError("Attempt context-header normalization evidence mismatch")
        environment_revision = canonical_sha256(
            {
                "base": fresh["environment_revision"],
                "catalog": state["catalog_sha256"],
                "live_environment": live_environment,
                "executor_context_header_normalizations": expected_header_normalizations,
            }
        )
        if (
            state.get("environment_revision") != environment_revision
            or state.get("provenance", {}).get("environment_revision") != environment_revision
        ):
            raise ValueError("Attempt environment revision binding mismatch")
    elif state.get("status") in {"IN_PROGRESS", "RECORDED_PENDING_VERIFICATION", "RECORDED_PENDING_REVIEW", "ACCEPTED"}:
        raise ValueError("Active or accepted attempt lacks captured catalog evidence")
    session_ids = state.get("mcp_session_ids", {})
    if not isinstance(session_ids, dict) or any(key not in fresh["environment_contract"]["servers"] for key in session_ids):
        raise ValueError("Attempt MCP session state is malformed")
    lifecycle = state.get("database_lifecycle")
    databases = state.get("databases")
    if not isinstance(lifecycle, dict) or not isinstance(databases, dict):
        raise ValueError("Attempt database lifecycle evidence is missing")
    if databases and set(databases) != set(fresh["environment_contract"]["servers"]):
        raise ValueError("Attempt database set differs from the canonical environment")
    for gym_name, database_id in databases.items():
        item = lifecycle.get(gym_name)
        if not isinstance(item, dict) or item.get("database_id") != database_id:
            raise ValueError("Attempt database lifecycle identity mismatch")
    _validate_transcript_prefix(state, fresh)
    state["task_bundle"] = fresh
    return state


def _load_state(attempt_id: str) -> tuple[Path, dict[str, Any], AppendOnlyAttemptLog]:
    directory = _attempt_dir(attempt_id)
    state = strict_json_loads((directory / "state.json").read_text(encoding="utf-8"))
    state = _freshen_and_validate_state(directory, state)
    log = AppendOnlyAttemptLog(directory, create=False)
    rows = log.read()
    evidence = state.get("execution_evidence")
    if evidence is not None:
        if not isinstance(evidence, dict):
            raise ValueError("Attempt execution evidence is malformed")
        expected_evidence = {
            "catalog_sha256": state.get("catalog_sha256"),
            "live_environment_sha256": canonical_sha256(state.get("live_environment")),
            "database_lifecycle_sha256": canonical_sha256(state.get("database_lifecycle")),
            "verifier_contract_sha256": state["task_bundle"]["verifier_contract_sha256"],
            "model_visible_sha256": canonical_sha256(
                {"messages": state.get("messages"), "tools": state.get("tools")}
            ),
        }
        if any(evidence.get(key) != value for key, value in expected_evidence.items()):
            raise ValueError("Attempt execution evidence no longer matches state")
        if state.get("status") == "RECORDED_PENDING_REVIEW" and evidence.get("event_log_head_sha256") != log.head_sha256:
            recoverable_publication = (
                (directory / "acceptance.journal.json").is_file()
                and rows
                and rows[-1].get("event_type") == "accepted_artifacts_written"
                and rows[-1].get("previous_event_sha256") == evidence.get("event_log_head_sha256")
            )
            recoverable_review = (
                isinstance(state.get("review_inflight"), dict)
                and rows
                and rows[-1].get("event_type") == "independent_review"
                and rows[-1].get("review") == state.get("review_inflight")
                and rows[-1].get("previous_event_sha256") == evidence.get("event_log_head_sha256")
            )
            if not recoverable_publication and not recoverable_review:
                raise ValueError("Attempt log changed after verification")
    if state.get("status") == "ACCEPTED" and state.get("publication_event_log_head_sha256") != log.head_sha256:
        raise ValueError("Accepted attempt log head mismatch")
    return directory, state, log


@contextmanager
def _locked_attempt(attempt_id: str):
    directory = _attempt_dir(attempt_id)
    with _exclusive_lock(directory / ".attempt.lock"):
        yield _load_state(attempt_id)


def _public_attempt(state: dict[str, Any]) -> dict[str, Any]:
    return {
        "attempt_id": state["attempt_id"],
        "source_task_id": state["source_task_id"],
        "status": state["status"],
        "messages": state["messages"],
        "tools": state["tools"],
        "outcomes": state.get("outcomes", []),
        "usage": state.get("usage"),
        "cleanup_success": state.get("cleanup_success"),
        "execution_evidence": copy.deepcopy(state.get("execution_evidence")),
        "provenance": state["provenance"],
    }


def _sanitized_attempt_snapshot(state: dict[str, Any], log: AppendOnlyAttemptLog) -> dict[str, Any]:
    """Exclude verifier SQL, context, database IDs, routing, and raw responses."""
    return {
        "schema_version": 1,
        "attempt_id": state.get("attempt_id"),
        "source_task_id": state.get("source_task_id"),
        "status": state.get("status"),
        "created_at": state.get("created_at"),
        "finished_at": state.get("finished_at"),
        "verified_at": state.get("verified_at"),
        "accepted_at": state.get("accepted_at"),
        "messages": copy.deepcopy(state.get("messages", [])),
        "tools": copy.deepcopy(state.get("tools", [])),
        "outcomes": copy.deepcopy(state.get("outcomes", [])),
        "usage": copy.deepcopy(state.get("usage")),
        "cost_usd": state.get("cost_usd"),
        "cost_status": state.get("cost_status"),
        "cleanup_success": state.get("cleanup_success"),
        "capture_protocol": state.get("capture_protocol"),
        "teacher_identity_status": state.get("teacher_identity_status"),
        "isolation": copy.deepcopy(state.get("isolation")),
        "provenance": copy.deepcopy(state.get("provenance")),
        "event_log_head_sha256": log.head_sha256,
        "note": "Sanitized snapshot; privileged executor state and verifier details are intentionally omitted.",
    }


def _pending_cleanup_databases(state: dict[str, Any]) -> dict[str, str]:
    lifecycle = state.get("database_lifecycle", {})
    return {
        gym_name: database_id
        for gym_name, database_id in state.get("databases", {}).items()
        if lifecycle.get(gym_name, {}).get("seed_status") in {"inflight", "succeeded"}
        and lifecycle.get(gym_name, {}).get("cleanup_status") != "succeeded"
    }


def _cleanup_attempt_databases(
    directory: Path, state: dict[str, Any], log: AppendOnlyAttemptLog
) -> bool:
    pending = _pending_cleanup_databases(state)
    if not pending:
        state["cleanup_success"] = True
        return True
    runtime = HTTPTaskRuntime(
        state["task_bundle"],
        attempt_id=state["attempt_id"],
        databases=pending,
        routing=state.get("routing", {}),
        session_ids=state.get("mcp_session_ids", {}),
    )

    def record(detail: dict[str, Any]) -> None:
        gym_name = detail["gym_name"]
        lifecycle = state["database_lifecycle"][gym_name]
        lifecycle["cleanup_status"] = "succeeded" if detail["success"] else "failed"
        lifecycle["cleanup_observed_at"] = utc_now()
        if detail.get("error"):
            lifecycle["cleanup_error"] = detail["error"]
        else:
            lifecycle.pop("cleanup_error", None)
        log.append({"event_type": "database_cleanup", **detail, "observed_at": utc_now()})
        _write_state(directory / "state.json", state)

    try:
        runtime.cleanup(on_result=record)
    except CleanupError as exc:
        state["cleanup_success"] = False
        state["cleanup_error"] = str(exc)
        _write_state(directory / "state.json", state)
        return False
    state["cleanup_success"] = not _pending_cleanup_databases(state)
    state.pop("cleanup_error", None)
    _write_state(directory / "state.json", state)
    return bool(state["cleanup_success"])


def _seal_terminal_attempt(
    directory: Path, state: dict[str, Any], log: AppendOnlyAttemptLog
) -> None:
    """Write a sanitized read-only snapshot after the final log event."""
    _atomic_json(directory / "attempt.json", _sanitized_attempt_snapshot(state, log), mode=0o400)
    os.chmod(log.path, 0o400)
    os.chmod(directory / "state.json", 0o400)


def command_setup(args: argparse.Namespace) -> int:
    bundle = load_task_bundle(args.task_id)
    attempt_id = f"{args.task_id}__{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}__{uuid.uuid4().hex[:10]}"
    directory = ATTEMPTS_ROOT / args.task_id / attempt_id
    log = AppendOnlyAttemptLog(directory, create=True)
    runtime = HTTPTaskRuntime(bundle, attempt_id=attempt_id)
    for gym_name in runtime.configs:
        runtime._headers(gym_name, include_database=False)
    header_normalizations = copy.deepcopy(runtime.context_header_normalizations)
    state: dict[str, Any] = {
        "attempt_id": attempt_id,
        "source_task_id": args.task_id,
        "status": "INITIALIZING",
        "created_at": utc_now(),
        "task_bundle": bundle,
        "messages": [
            {"role": "system", "content": bundle["task_input"]["system_prompt"]},
            {"role": "user", "content": bundle["task_input"]["user_prompt"]},
        ],
        "tools": [],
        "databases": {},
        "database_lifecycle": {},
        "routing": {},
        "mcp_session_ids": {},
        "outcomes": [],
        "verification_details": [],
        "usage": None,
        "cost_usd": None,
        "cost_status": "unknown_provider_cost_not_reported",
        "executor_context_header_normalizations": header_normalizations,
        "capture_protocol": "solver_submitted_assistant_envelope_v2",
        "teacher_identity_status": "operator_label_only_provider_identity_not_reported",
        "state_integrity_status": "unkeyed_sha256_detects_accidental_change_only",
        "isolation": {
            "fresh_solver_context_requested": True,
            "model_visible_bundle_limited_to_canonical_messages_and_selected_live_schemas": True,
            "gateway_restricts_calls_to_selected_tools": True,
            "os_level_solver_filesystem_isolation": False,
            "note": "Solver contexts share the host filesystem capability; compliance is instruction- and gateway-enforced, not an OS security boundary.",
        },
        "provenance": {
            "teacher_model": args.teacher_model,
            "generator_revision": bundle["generator_revision"],
            "environment_revision": bundle["environment_revision"],
            "source_trace_id": attempt_id,
        },
    }
    with _exclusive_lock(directory / ".attempt.lock"):
        log.append({"event_type": "attempt_started", "attempt_id": attempt_id, "source_task_id": args.task_id, "created_at": utc_now()})
        if header_normalizations:
            log.append(
                {
                    "event_type": "executor_context_headers_normalized",
                    "normalizations": header_normalizations,
                    "policy": "server_specific_header_name_only_token_value_unchanged_v1",
                    "observed_at": utc_now(),
                }
            )
        _write_state(directory / "state.json", state)
        try:
            live_environment = runtime.attest_live_environment()
            state["live_environment"] = live_environment
            log.append({"event_type": "live_environment_attested", "evidence": live_environment, "observed_at": utc_now()})
            databases = runtime.plan_databases()
            state["databases"] = databases
            state["database_lifecycle"] = {
                gym_name: {
                    "database_id": database_id,
                    "seed_status": "planned",
                    "cleanup_status": "pending",
                }
                for gym_name, database_id in databases.items()
            }
            log.append({"event_type": "database_ids_planned", "database_ids": databases, "observed_at": utc_now()})
            _write_state(directory / "state.json", state)

            def record_seed_start(gym_name: str, database_id: str) -> None:
                lifecycle = state["database_lifecycle"][gym_name]
                lifecycle["seed_status"] = "inflight"
                lifecycle["seed_started_at"] = utc_now()
                log.append({"event_type": "database_seed_started", "gym_name": gym_name, "database_id": database_id, "observed_at": utc_now()})
                _write_state(directory / "state.json", state)

            def record_seed(detail: dict[str, Any]) -> None:
                lifecycle = state["database_lifecycle"][detail["gym_name"]]
                lifecycle["seed_status"] = "succeeded"
                lifecycle["seed_evidence"] = detail
                log.append({"event_type": "database_seeded", **detail, "observed_at": utc_now()})
                _write_state(directory / "state.json", state)

            runtime.seed_all(on_seed_start=record_seed_start, on_seed=record_seed)
            if any(item["seed_status"] != "succeeded" for item in state["database_lifecycle"].values()):
                raise RuntimeError("Not every planned database was confirmed seeded")
            tools, routing, catalog_sha, catalog_record = runtime.discover_selected_tools(bundle["task_input"]["selected_tools"])
            validate_solver_response(
                {"role": "assistant", "content": "catalog-validation"},
                tools,
                selected_tool_names=bundle["task_input"]["selected_tools"],
            )
            state["tools"] = tools
            state["routing"] = routing
            state["mcp_session_ids"] = dict(runtime.session_ids)
            state["catalog_sha256"] = catalog_sha
            state["environment_revision"] = canonical_sha256(
                {
                    "base": bundle["environment_revision"],
                    "catalog": catalog_sha,
                    "live_environment": live_environment,
                    "executor_context_header_normalizations": header_normalizations,
                }
            )
            state["provenance"]["environment_revision"] = state["environment_revision"]
            state["status"] = "IN_PROGRESS"
            _atomic_json(directory / "catalog.executor-only.json", catalog_record)
            log.append({"event_type": "tool_catalog_captured", "catalog_sha256": catalog_sha, "selected_tool_names": [_tool_name(t) for t in tools], "observed_at": utc_now()})
            solver_bundle = {
                "attempt_id": attempt_id,
                "messages": copy.deepcopy(state["messages"]),
                "tools": copy.deepcopy(tools),
                "usage_contract": "Use only the visible tools through the restricted step command; do not inspect other workspace files.",
                "capture_protocol": "Submit each exact assistant message as one native function-call envelope through the restricted step command.",
                "isolation_notice": "No OS-level filesystem isolation is available; compliance is procedural and will be reviewed.",
            }
            _atomic_json(directory / "solver_bundle.json", solver_bundle, mode=0o600)
            _write_state(directory / "state.json", state)
            print(json.dumps({"attempt_id": attempt_id, "status": state["status"], "solver_bundle": str(directory / "solver_bundle.json")}, indent=2))
            return 0
        except Exception as exc:
            state["status"] = "BLOCKED_BACKEND"
            state["error"] = str(exc)
            state["databases"] = dict(runtime.databases)
            log.append({"event_type": "attempt_error", "error": str(exc), "observed_at": utc_now()})
            _write_state(directory / "state.json", state)
            cleanup_ok = _cleanup_attempt_databases(directory, state, log)
            log.append({"event_type": "attempt_finished", "status": state["status"], "finished_at": utc_now()})
            _write_state(directory / "state.json", state)
            if cleanup_ok:
                _seal_terminal_attempt(directory, state, log)
            print(json.dumps({"attempt_id": attempt_id, "status": state["status"], "error": str(exc)}, indent=2))
            return 2


def command_step(args: argparse.Namespace) -> int:
    with _locked_attempt(args.attempt_id) as (directory, state, log):
        return _command_step_locked(args, directory, state, log)


def _command_step_locked(
    args: argparse.Namespace,
    directory: Path,
    state: dict[str, Any],
    log: AppendOnlyAttemptLog,
) -> int:
    """Capture one exact solver assistant envelope, then execute all its calls."""
    if state["status"] != "IN_PROGRESS":
        raise ValueError(f"Attempt is not callable: {state['status']}")
    if state.get("capture_protocol") != "solver_submitted_assistant_envelope_v2":
        raise ValueError("This attempt predates exact assistant-envelope capture")
    if state.get("inflight_step"):
        raise ValueError("A prior tool step was interrupted; abort this attempt rather than replaying it")
    response = strict_json_loads(args.message)
    existing_ids = tuple(
        call["id"]
        for message in state["messages"]
        if isinstance(message, dict)
        for call in message.get("tool_calls", [])
    )
    validate_solver_response(
        response,
        state["tools"],
        pending_call_ids=existing_ids,
        selected_tool_names=state["task_bundle"]["task_input"]["selected_tools"],
    )
    usage = response.get("usage")
    visible_message = {
        key: copy.deepcopy(value)
        for key, value in response.items()
        if key in {"role", "content", "reasoning_content", "tool_calls"}
    }
    visible_message.setdefault("content", "")
    state["messages"].append(visible_message)
    if usage is not None:
        state["usage"] = usage
    log.append(
        {
            "event_type": "assistant_message",
            "message": visible_message,
            "usage": usage,
            "capture": "solver_submitted_exact_envelope",
            "observed_at": utc_now(),
        }
    )
    calls = visible_message.get("tool_calls", [])
    if not calls:
        state["status"] = "RECORDED_PENDING_VERIFICATION"
        state["finished_at"] = utc_now()
        log.append({"event_type": "solver_finished", "status": state["status"], "finished_at": state["finished_at"]})
        _write_state(directory / "state.json", state)
        print(json.dumps({"attempt_id": args.attempt_id, "status": state["status"], "tool_results": []}, ensure_ascii=False, indent=2))
        return 0
    runtime = HTTPTaskRuntime(
        state["task_bundle"],
        attempt_id=state["attempt_id"],
        databases=state["databases"],
        routing=state["routing"],
        session_ids=state.get("mcp_session_ids", {}),
    )
    observed_environment = runtime.attest_live_environment()
    if observed_environment != state.get("live_environment"):
        raise RuntimeError("Live benchmark containers changed during the attempt")
    state["inflight_step"] = {
        "assistant_message_sha256": canonical_sha256(visible_message),
        "calls": {call["id"]: "pending" for call in calls},
        "started_at": utc_now(),
    }
    _write_state(directory / "state.json", state)
    visible_results = []
    for call in calls:
        call_id = call["id"]
        tool_name = call["function"]["name"]
        arguments = call["function"]["arguments"]
        log.append({"event_type": "tool_call", "tool_call_id": call_id, "tool_name": tool_name, "arguments": arguments, "capture": "solver_submitted_exact_envelope", "observed_at": utc_now()})
        try:
            execution = runtime.call_tool(tool_name, arguments)
            raw_result = execution["result"]
            visible_result, redaction = runtime.model_visible_result(raw_result)
            if isinstance(raw_result, dict) and "isError" in raw_result and type(raw_result["isError"]) is not bool:
                raise RuntimeError("MCP tool result has a non-boolean isError field")
            tool_success = not (
                isinstance(raw_result, dict) and raw_result.get("isError") is True
            )
            execution["transport"]["model_visible_projection"] = redaction
            log.append(
                {
                    "event_type": "tool_result",
                    "tool_call_id": call_id,
                    "tool_name": tool_name,
                    "rpc_success": True,
                    "tool_success": tool_success,
                    "raw_response": execution["raw_response"],
                    "parsed_result": raw_result,
                    "model_visible_result": visible_result,
                    "transport": execution["transport"],
                    "observed_at": utc_now(),
                }
            )
        except Exception as exc:
            sanitized_error, redaction_count = _redact_executor_metadata(str(exc), list(runtime.databases.values()))
            visible_result = {"isError": True, "error": sanitized_error}
            log.append({"event_type": "tool_result", "tool_call_id": call_id, "tool_name": tool_name, "rpc_success": False, "tool_success": False, "error": str(exc), "observed_at": utc_now()})
        tool_message = {
            "role": "tool",
            "tool_call_id": call_id,
            "name": tool_name,
            "content": canonical_json(visible_result),
        }
        state["messages"].append(tool_message)
        state["mcp_session_ids"] = dict(runtime.session_ids)
        state["inflight_step"]["calls"][call_id] = "recorded"
        _write_state(directory / "state.json", state)
        visible_results.append({"tool_call_id": call_id, "tool_name": tool_name, "response": visible_result})
    state.pop("inflight_step", None)
    _write_state(directory / "state.json", state)
    print(json.dumps({"attempt_id": args.attempt_id, "status": state["status"], "tool_results": visible_results}, ensure_ascii=False, indent=2))
    return 0


def command_verify(args: argparse.Namespace) -> int:
    with _locked_attempt(args.attempt_id) as (directory, state, log):
        return _command_verify_locked(args, directory, state, log)


def _command_verify_locked(
    args: argparse.Namespace,
    directory: Path,
    state: dict[str, Any],
    log: AppendOnlyAttemptLog,
) -> int:
    if state["status"] != "RECORDED_PENDING_VERIFICATION":
        raise ValueError(f"Attempt is not pending verification: {state['status']}")
    if state.get("inflight_step"):
        raise ValueError("Interrupted tool execution cannot be verified")
    runtime = HTTPTaskRuntime(
        state["task_bundle"],
        attempt_id=state["attempt_id"],
        databases=state["databases"],
        routing=state["routing"],
        session_ids=state.get("mcp_session_ids", {}),
    )
    observed_environment = runtime.attest_live_environment()
    if observed_environment != state.get("live_environment"):
        raise RuntimeError("Live benchmark containers changed before verification")
    outcomes = []
    details = []
    try:
        for index, verifier in enumerate(state["task_bundle"]["verifiers"]):
            config = verifier.get("validation_config", {})
            try:
                execution = runtime.run_sql(verifier.get("gym_name"), config["query"])
                raw, result = execution["raw_response"], execution["result"]
                actual = extract_sql_value(result)
                passed = compare_values(actual, config.get("expected_value"), config.get("comparison_type", "equals"))
                error = None
            except Exception as exc:
                raw, result, actual, passed, error = None, None, None, False, str(exc)
            outcome = {
                "verifier_index": index,
                "verifier_name": verifier["name"],
                "passed": bool(passed),
                "error": error,
            }
            outcomes.append(outcome)
            detail = {
                **outcome,
                "comparison_type": config.get("comparison_type", "equals"),
                "expected": config.get("expected_value"),
                "actual": actual,
                "query": config.get("query"),
                "raw_response": raw,
                "parsed_response": result,
                "transport": execution.get("transport") if error is None else None,
                "gym_name": verifier.get("gym_name"),
            }
            details.append(detail)
            log.append({"event_type": "verifier_outcome", **detail, "observed_at": utc_now()})
        state["outcomes"] = outcomes
        state["verification_details"] = details
        all_passed = review_acceptance_ready(
            {"status": "accepted", "reviewer": "verification-gate", "reviewed_at": utc_now(), "no_evaluation_or_privileged_content": True},
            outcomes,
            len(state["task_bundle"]["verifiers"]),
        )
        state["status"] = "RECORDED_PENDING_CLEANUP"
        _write_state(directory / "state.json", state)
    except Exception:
        state["status"] = "ATTEMPT_FAILED"
        _write_state(directory / "state.json", state)
        _cleanup_attempt_databases(directory, state, log)
        raise
    cleanup_ok = _cleanup_attempt_databases(directory, state, log)
    state["status"] = "RECORDED_PENDING_REVIEW" if all_passed and cleanup_ok else "ATTEMPT_FAILED"
    state["verified_at"] = utc_now()
    log.append({"event_type": "attempt_finished", "status": state["status"], "finished_at": state["verified_at"]})
    state["execution_evidence"] = {
        "event_log_head_sha256": log.head_sha256,
        "catalog_sha256": state["catalog_sha256"],
        "live_environment_sha256": canonical_sha256(state["live_environment"]),
        "database_lifecycle_sha256": canonical_sha256(state["database_lifecycle"]),
        "verifier_contract_sha256": state["task_bundle"]["verifier_contract_sha256"],
        "model_visible_sha256": canonical_sha256(
            {"messages": state["messages"], "tools": state["tools"]}
        ),
        "integrity_scope": "unkeyed local hashes; no external signature or OS solver boundary",
    }
    _write_state(directory / "state.json", state)
    if state["status"] == "ATTEMPT_FAILED":
        _seal_terminal_attempt(directory, state, log)
    print(json.dumps({"attempt_id": args.attempt_id, "status": state["status"], "checks_total": len(outcomes), "checks_passed": sum(1 for item in outcomes if item["passed"]), "outcomes": outcomes}, indent=2))
    return 0 if state["status"] == "RECORDED_PENDING_REVIEW" else 2


def command_abort(args: argparse.Namespace) -> int:
    with _locked_attempt(args.attempt_id) as (directory, state, log):
        if state["status"] == "ACCEPTED":
            raise ValueError("Accepted attempt cannot be aborted")
        cleanup_ok = _cleanup_attempt_databases(directory, state, log)
        state["status"] = "ATTEMPT_FAILED"
        state["error"] = args.reason
        log.append({"event_type": "attempt_finished", "status": state["status"], "reason": args.reason, "finished_at": utc_now()})
        _write_state(directory / "state.json", state)
        if cleanup_ok:
            _seal_terminal_attempt(directory, state, log)
        print(json.dumps({"attempt_id": args.attempt_id, "status": state["status"], "cleanup_success": cleanup_ok}, indent=2))
        return 0 if cleanup_ok else 2


def _existing_trace_ids() -> set[str]:
    if not REVIEWED_TRACES.is_file():
        return set()
    ids = set()
    with REVIEWED_TRACES.open(encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                row = strict_json_loads(line)
                if not isinstance(row, dict) or not isinstance(row.get("source_task_id"), str):
                    raise ValueError("Reviewed trace file contains a malformed row")
                ids.add(row["source_task_id"])
    return ids


def _existing_trace_hashes() -> dict[str, str]:
    if not REVIEWED_TRACES.is_file():
        return {}
    found: dict[str, str] = {}
    with REVIEWED_TRACES.open(encoding="utf-8") as handle:
        for line in handle:
            if not line.strip():
                continue
            row = strict_json_loads(line)
            if not isinstance(row, dict) or not isinstance(row.get("source_task_id"), str):
                raise ValueError("Reviewed trace file contains a malformed row")
            task_id = row["source_task_id"]
            if task_id in found:
                raise ValueError("Reviewed trace file contains duplicate task IDs")
            found[task_id] = canonical_sha256(row)
    return found


def _journal_digest(journal: dict[str, Any]) -> str:
    return canonical_sha256({key: value for key, value in journal.items() if key != "journal_sha256"})


def _write_acceptance_journal(path: Path, journal: dict[str, Any], *, create: bool = False) -> None:
    journal["journal_sha256"] = _journal_digest(journal)
    if create:
        _exclusive_bytes(path, _pretty_json_bytes(journal), mode=0o600)
    else:
        _atomic_json(path, journal, mode=0o600)


def _load_acceptance_journal(path: Path) -> dict[str, Any]:
    journal = strict_json_loads(path.read_text(encoding="utf-8"))
    if not isinstance(journal, dict) or journal.get("journal_sha256") != _journal_digest(journal):
        raise ValueError("Acceptance journal integrity mismatch")
    return journal


def _publish_acceptance_journal(
    directory: Path,
    state: dict[str, Any],
    log: AppendOnlyAttemptLog,
    journal: dict[str, Any],
) -> int:
    task_id = state["source_task_id"]
    if journal.get("source_task_id") != task_id:
        raise ValueError("Acceptance journal task mismatch")
    receipt = journal.get("receipt")
    trace = journal.get("trace")
    if not isinstance(receipt, dict) or not isinstance(trace, dict):
        raise ValueError("Acceptance journal payload is malformed")
    receipt_path = RECEIPTS_ROOT / f"{task_id}.json"
    receipt_bytes = _pretty_json_bytes(receipt)
    receipt_sha = hashlib.sha256(receipt_bytes).hexdigest()
    if journal.get("receipt_sha256") != receipt_sha:
        raise ValueError("Acceptance journal receipt digest mismatch")
    if trace.get("review", {}).get("verifier_receipt", {}).get("sha256") != receipt_sha:
        raise ValueError("Acceptance journal trace/receipt binding mismatch")
    trace_sha = canonical_sha256(trace)
    if journal.get("trace_sha256") != trace_sha:
        raise ValueError("Acceptance journal trace digest mismatch")

    with _exclusive_lock(ACCEPTANCE_LOCK):
        existing = _existing_trace_hashes()
        existing_trace = existing.get(task_id)
        if existing_trace is not None and existing_trace != trace_sha:
            raise ValueError("A different accepted trace already exists for this task")
        if receipt_path.exists():
            if sha256_file(receipt_path) != receipt_sha:
                raise FileExistsError("A different verifier receipt already exists")
        else:
            _exclusive_bytes(receipt_path, receipt_bytes, mode=0o600)
        if existing_trace is None:
            _append_bytes(REVIEWED_TRACES, (canonical_json(trace) + "\n").encode("utf-8"), mode=0o600)
        journal["phase"] = "PUBLISHED"
        journal["published_at"] = utc_now()
        _write_acceptance_journal(directory / "acceptance.journal.json", journal)

    state["status"] = "ACCEPTED"
    state["review"] = copy.deepcopy(journal["review"])
    state["receipt"] = {
        "path": f"receipts/{receipt_path.name}",
        "sha256": receipt_sha,
    }
    state["accepted_at"] = journal.get("published_at", utc_now())
    already_logged = any(
        row.get("event_type") == "accepted_artifacts_written"
        and row.get("receipt", {}).get("sha256") == receipt_sha
        for row in log.read()
    )
    if not already_logged:
        log.append(
            {
                "event_type": "accepted_artifacts_written",
                "receipt": state["receipt"],
                "reviewed_traces_path": str(REVIEWED_TRACES.relative_to(ROOT)),
                "observed_at": utc_now(),
            }
        )
    state["publication_event_log_head_sha256"] = log.head_sha256
    _write_state(directory / "state.json", state)
    _seal_terminal_attempt(directory, state, log)
    print(json.dumps({"attempt_id": state["attempt_id"], "status": state["status"], "receipt": str(receipt_path), "trace_file": str(REVIEWED_TRACES)}, indent=2))
    return 0


def command_review(args: argparse.Namespace) -> int:
    with _locked_attempt(args.attempt_id) as (directory, state, log):
        journal_path = directory / "acceptance.journal.json"
        if journal_path.is_file():
            return _publish_acceptance_journal(
                directory, state, log, _load_acceptance_journal(journal_path)
            )
        if state.get("status") != "RECORDED_PENDING_REVIEW" or state.get("cleanup_success") is not True:
            raise ValueError("Only a fully verified and cleaned attempt may receive review")
        review = state.get("review_inflight")
        if review is None:
            review = {
                "status": "accepted" if args.accept else "rejected",
                "reviewer": args.reviewer,
                "reviewed_at": utc_now(),
                "no_evaluation_or_privileged_content": bool(args.confirm_no_privileged_content),
            }
            if args.notes:
                review["notes"] = args.notes
            state["review_inflight"] = copy.deepcopy(review)
            _write_state(directory / "state.json", state)
        elif (
            review.get("status") != ("accepted" if args.accept else "rejected")
            or review.get("reviewer") != args.reviewer
        ):
            raise ValueError("Review retry differs from the journaled decision")
        if args.accept and review["no_evaluation_or_privileged_content"] is not True:
            raise ValueError("Acceptance requires explicit no-privileged-content confirmation")
        review_logged = any(
            row.get("event_type") == "independent_review" and row.get("review") == review
            for row in log.read()
        )
        if not review_logged:
            log.append({"event_type": "independent_review", "review": review, "observed_at": utc_now()})
        state["execution_evidence"]["event_log_head_sha256"] = log.head_sha256
        _write_state(directory / "state.json", state)
        if not args.accept:
            state["status"] = "REVIEW_REJECTED"
            state["review"] = review
            state.pop("review_inflight", None)
            log.append({"event_type": "attempt_finished", "status": state["status"], "finished_at": utc_now()})
            _write_state(directory / "state.json", state)
            _seal_terminal_attempt(directory, state, log)
            print(json.dumps({"attempt_id": args.attempt_id, "status": state["status"]}, indent=2))
            return 0
        fresh_bundle = load_task_bundle(state["source_task_id"])
        if _contract_view(fresh_bundle) != _contract_view(state["task_bundle"]):
            raise ValueError("Frozen training contract changed before review")
        state["task_bundle"] = fresh_bundle
        attempt = _public_attempt(state)
        receipt = build_receipt(fresh_bundle, attempt, state["outcomes"], review)
        receipt_bytes = _pretty_json_bytes(receipt)
        receipt_sha = hashlib.sha256(receipt_bytes).hexdigest()
        receipt_ref = {"path": f"receipts/{state['source_task_id']}.json", "sha256": receipt_sha}
        trace = build_reviewed_trace(fresh_bundle, attempt, receipt_ref, review)
        journal = {
            "schema_version": 1,
            "phase": "PREPARED",
            "source_task_id": state["source_task_id"],
            "attempt_id": state["attempt_id"],
            "review": review,
            "receipt": receipt,
            "receipt_sha256": receipt_sha,
            "trace": trace,
            "trace_sha256": canonical_sha256(trace),
            "prepared_at": utc_now(),
        }
        _write_acceptance_journal(journal_path, journal, create=True)
        return _publish_acceptance_journal(directory, state, log, journal)


def command_status(args: argparse.Namespace) -> int:
    with _locked_attempt(args.attempt_id) as (_, state, _):
        public = {
            key: state.get(key)
            for key in (
                "attempt_id",
                "source_task_id",
                "status",
                "created_at",
                "finished_at",
                "verified_at",
                "accepted_at",
                "usage",
                "cost_usd",
                "cost_status",
                "outcomes",
                "cleanup_success",
                "error",
            )
            if key in state
        }
        print(json.dumps(public, indent=2))
        return 0


def command_seal(args: argparse.Namespace) -> int:
    with _locked_attempt(args.attempt_id) as (directory, state, log):
        if state.get("status") not in {"ATTEMPT_FAILED", "REVIEW_REJECTED", "ACCEPTED", "BLOCKED_BACKEND"}:
            raise ValueError("Only terminal attempts may be sealed")
        if state.get("cleanup_success") is not True:
            raise ValueError("Attempt cannot be sealed until cleanup is confirmed")
        if not (directory / "attempt.json").exists():
            log.append({"event_type": "attempt_sealed", "status": state["status"], "observed_at": utc_now()})
            _seal_terminal_attempt(directory, state, log)
        print(json.dumps({"attempt_id": args.attempt_id, "status": state["status"], "sealed": True}, indent=2))
        return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    setup = commands.add_parser("setup", help="Seed a fresh training-only attempt and capture selected live schemas")
    setup.add_argument("--task-id", required=True)
    setup.add_argument("--teacher-model", required=True)
    setup.set_defaults(func=command_setup)
    step = commands.add_parser("step", help="Capture one exact solver assistant envelope and execute all selected calls in it")
    step.add_argument("--attempt-id", required=True)
    step.add_argument("--message", required=True, help="JSON assistant message object")
    step.set_defaults(func=command_step)
    verify = commands.add_parser("verify", help="Run every indexed verifier and clean up attempt databases")
    verify.add_argument("--attempt-id", required=True)
    verify.set_defaults(func=command_verify)
    abort = commands.add_parser("abort", help="Preserve a failed attempt and clean up its databases")
    abort.add_argument("--attempt-id", required=True)
    abort.add_argument("--reason", required=True)
    abort.set_defaults(func=command_abort)
    review = commands.add_parser("review", help="Record independent semantic review and optionally emit accepted artifacts")
    review.add_argument("--attempt-id", required=True)
    review.add_argument("--reviewer", required=True)
    decision = review.add_mutually_exclusive_group(required=True)
    decision.add_argument("--accept", action="store_true")
    decision.add_argument("--reject", action="store_true")
    review.add_argument("--confirm-no-privileged-content", action="store_true")
    review.add_argument("--notes")
    review.set_defaults(func=command_review)
    status = commands.add_parser("status")
    status.add_argument("--attempt-id", required=True)
    status.set_defaults(func=command_status)
    seal = commands.add_parser("seal", help="Seal an already-terminal attempt created by an earlier harness revision")
    seal.add_argument("--attempt-id", required=True)
    seal.set_defaults(func=command_seal)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        return int(args.func(args))
    except Exception as exc:
        print(json.dumps({"error": str(exc), "command": args.command}, indent=2), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
