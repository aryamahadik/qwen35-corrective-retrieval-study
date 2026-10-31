#!/usr/bin/env python3
"""Validate reviewed training-only traces and prepare explicit assistant labels.

No teacher calls, SQL execution, GPU work, or gold trajectories are generated.
An accepted external review/receipt is supplied provenance, not proof that this
script independently reproduced the verifier. Use --validate-only before paying
for tokenizer/model setup. The full trace contract is in config/trace_schema.json.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import importlib.metadata
import json
from pathlib import Path
import re
import shutil
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
MODEL_ID = "Qwen/Qwen3.5-9B"
MODEL_REVISION = "c202236235762e1c871ad0ccb60c8ee5ba337b9a"
TEMPLATE_PATH = ROOT / "config" / "qwen3_5_think_training.jinja"
TEMPLATE_SOURCE = "https://github.com/huggingface/trl/blob/63b7c3f547d3e06d0eae72712e36b7b64e9d5a45/trl/chat_templates/qwen3_5_think_training.jinja"
TEMPLATE_SHA256 = "ccf356d8f238e287c047b1ef589850fd6b2b44e6cb29079e26c635fb9b8111ef"
TRAINING_CONTRACTS_PATH = ROOT / "data" / "evaluator_only" / "train.jsonl"
TRAINING_INPUTS_PATH = ROOT / "data" / "task_inputs" / "train.jsonl"
TOKENIZER_DIRECTORY = ROOT / "data" / "tokenizer" / "model"
TASK_INPUT_FIELDS = ("task_id", "domain", "system_prompt", "user_prompt", "selected_tools", "restricted_tools")
RECEIPT_SCHEMA_VERSION = 2
EXPECTED_VERSIONS = {"transformers": "5.5.0", "tokenizers": "0.22.2", "jinja2": "3.1.6"}
SHA = re.compile(r"[0-9a-f]{64}\Z")
NAME = re.compile(r"[A-Za-z_][A-Za-z0-9_.-]*\Z")
ADMIN_FIELDS = {
    "sql", "sql_query", "verifier", "verifiers", "verification", "gold_answer",
    "gold_actions", "ground_truth", "expected_result", "expected_state",
    "admin_state", "admin_query", "admin_sql",
}
RESERVED_MARKERS = ("<|im_start|>", "<|im_end|>", "<|endoftext|>")


class PreparationError(ValueError):
    """Input cannot be published as the reviewed training dataset."""


def sha256_file(path) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def canonical_sha256(value) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":"),
                                    ensure_ascii=False, allow_nan=False).encode()).hexdigest()


def _json_loads(text):
    """Reject ambiguous duplicate keys and non-JSON NaN/Infinity values."""
    def unique_object(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise PreparationError(f"Duplicate JSON object key: {key}")
            result[key] = value
        return result
    def invalid_constant(value):
        raise PreparationError(f"Invalid JSON numeric constant: {value}")
    return json.loads(text, object_pairs_hook=unique_object, parse_constant=invalid_constant)


def _nonempty(value, field):
    if not isinstance(value, str) or not value.strip():
        raise PreparationError(f"Missing/empty {field}")
    return value


def _reject_admin_keys(value):
    if isinstance(value, dict):
        for key, child in value.items():
            if str(key).lower() in ADMIN_FIELDS or str(key).lower().startswith("admin_"):
                raise PreparationError(f"Privileged field in model-visible payload: {key}")
            _reject_admin_keys(child)
    elif isinstance(value, list):
        for child in value:
            _reject_admin_keys(child)


def _reject_role_controls(value):
    if isinstance(value, str):
        if any(marker in value for marker in RESERVED_MARKERS):
            raise PreparationError("Role-control tokens are not permitted in model-visible fields")
    elif isinstance(value, dict):
        for key, child in value.items():
            _reject_role_controls(key)
            _reject_role_controls(child)
    elif isinstance(value, list):
        for child in value:
            _reject_role_controls(child)


def model_payload(record) -> dict:
    """Whitelist model-visible fields; never serialize the entire source record."""
    messages, tools = record.get("messages"), record.get("tools")
    if not isinstance(messages, list) or not messages:
        raise PreparationError("messages must be a complete nonempty conversation")
    if not isinstance(tools, list):
        raise PreparationError("tools must be the actual visible tool-schema list")
    _reject_admin_keys({"messages": messages, "tools": tools})
    _reject_role_controls({"messages": messages, "tools": tools})
    clean_tools, tool_names = [], set()
    for tool in tools:
        if not isinstance(tool, dict) or set(tool) != {"type", "function"} or tool["type"] != "function":
            raise PreparationError("Tools must use the {type:function,function:{...}} schema")
        function = tool["function"]
        if not isinstance(function, dict) or set(function) - {"name", "description", "parameters", "strict"}:
            raise PreparationError("Tool function contains unsupported fields")
        name = function.get("name")
        if not isinstance(name, str) or not NAME.fullmatch(name) or name in tool_names:
            raise PreparationError("Tool names must be unique safe identifiers")
        if not isinstance(function.get("parameters"), dict):
            raise PreparationError("Every tool requires an explicit parameters schema")
        tool_names.add(name)
        clean_tools.append(tool)
    clean_messages, pending, seen_calls = [], {}, set()
    user_seen = False
    for index, message in enumerate(messages):
        if not isinstance(message, dict):
            raise PreparationError("Each message must be an object")
        role = message.get("role")
        allowed = {"role", "content"}
        if role == "assistant":
            allowed |= {"reasoning_content", "tool_calls"}
        elif role == "tool":
            allowed |= {"tool_call_id", "name"}
        if role not in {"system", "user", "assistant", "tool"} or set(message) - allowed:
            raise PreparationError("Message contains unsupported role/fields")
        content = message.get("content", "")
        if not isinstance(content, str) or any(marker in content for marker in RESERVED_MARKERS):
            raise PreparationError("Only plain text content without role-control tokens is supported")
        if role != "assistant" and not content.strip():
            raise PreparationError("System/user/tool messages require nonempty content")
        if role == "system" and index != 0:
            raise PreparationError("System message is only permitted at the beginning")
        if pending and role != "tool":
            raise PreparationError("Conversation is missing one or more tool responses")
        if role == "user":
            user_seen = True
        if role == "assistant":
            if not user_seen:
                raise PreparationError("Assistant response appears before a user query")
            if index > 0 and messages[index - 1].get("role") == "assistant":
                raise PreparationError("Consecutive assistant turns lack an intervening observation")
            reasoning = message.get("reasoning_content", "")
            if not isinstance(reasoning, str) or any(marker in reasoning for marker in RESERVED_MARKERS):
                raise PreparationError("reasoning_content must be plain text")
            if "<think>" in content or "</think>" in content:
                raise PreparationError("Put reasoning in reasoning_content before external review")
            calls = message.get("tool_calls", [])
            if not isinstance(calls, list):
                raise PreparationError("tool_calls must be a list")
            if not content.strip() and not calls:
                raise PreparationError("Assistant target has neither an answer nor a tool call")
            for call in calls:
                if not isinstance(call, dict) or set(call) != {"id", "type", "function"} or call["type"] != "function":
                    raise PreparationError("Each tool call requires id, type, and function")
                call_id = _nonempty(call.get("id"), "tool call id")
                if call_id in seen_calls:
                    raise PreparationError("Tool call IDs must be unique within a workflow")
                function = call.get("function")
                if not isinstance(function, dict) or set(function) != {"name", "arguments"}:
                    raise PreparationError("Tool call function requires name and arguments")
                if (not isinstance(function["name"], str) or function["name"] not in tool_names
                        or not isinstance(function["arguments"], dict)):
                    raise PreparationError("Tool calls need a visible tool and parsed argument object")
                if any(not isinstance(key, str) or not NAME.fullmatch(key) for key in function["arguments"]):
                    raise PreparationError("Tool argument names must be safe identifiers")
                pending[call_id] = function["name"]
                seen_calls.add(call_id)
        if role == "tool":
            call_id = message.get("tool_call_id")
            if not isinstance(call_id, str) or call_id not in pending:
                raise PreparationError("Orphan/duplicate tool response")
            if message.get("name", pending[call_id]) != pending[call_id]:
                raise PreparationError("Tool response name does not match its call")
            del pending[call_id]
        clean_messages.append({key: value for key, value in message.items() if key in allowed})
    if pending or messages[-1].get("role") != "assistant" or messages[-1].get("tool_calls"):
        raise PreparationError("Workflow must include all tool results and a final assistant response")
    return {"messages": clean_messages, "tools": clean_tools}


def _task_input(record) -> dict:
    if not isinstance(record, dict) or any(key not in record for key in TASK_INPUT_FIELDS):
        raise PreparationError("Canonical task input is missing required fields")
    result = {key: record[key] for key in TASK_INPUT_FIELDS}
    for key in ("task_id", "domain", "system_prompt", "user_prompt"):
        _nonempty(result[key], f"task input {key}")
    for key in ("selected_tools", "restricted_tools"):
        names = result[key]
        if (not isinstance(names, list) or any(not isinstance(name, str) or not NAME.fullmatch(name) for name in names)
                or len(names) != len(set(names))):
            raise PreparationError("Canonical tool-name lists must contain unique safe identifiers")
    if set(result["selected_tools"]) & set(result["restricted_tools"]):
        raise PreparationError("Canonical task has a selected/restricted tool conflict")
    return result


def load_training_contracts(path, allowed_task_ids, task_inputs_path=TRAINING_INPUTS_PATH) -> dict:
    """Bind training-only public inputs to verifier identities, counts and hashes.

    Live tool schemas/argument semantics are not inferred from tool names. No
    held-out payload is read, and verifier SQL never enters returned model input.
    """
    inputs = {}
    with Path(task_inputs_path).open() as handle:
        for line in handle:
            if not line.strip():
                continue
            raw_input = _json_loads(line)
            if not isinstance(raw_input, dict) or set(raw_input) != set(TASK_INPUT_FIELDS):
                raise PreparationError("Canonical public task input contains unexpected fields")
            task_input = _task_input(raw_input)
            task_id = task_input["task_id"]
            if task_id not in allowed_task_ids or task_id in inputs:
                raise PreparationError("Public training inputs contain duplicate or non-training membership")
            inputs[task_id] = task_input
    if set(inputs) != set(allowed_task_ids):
        raise PreparationError("Public training inputs do not cover the frozen membership")
    contracts = {}
    with Path(path).open() as handle:
        for number, line in enumerate(handle, 1):
            if not line.strip():
                continue
            try:
                record = _json_loads(line)
            except ValueError as error:
                raise PreparationError(f"Invalid training contract at line {number}") from error
            task_id = record.get("task_id") if isinstance(record, dict) else None
            if not isinstance(task_id, str) or task_id not in allowed_task_ids or task_id in contracts:
                raise PreparationError("Training contracts contain duplicate or non-training membership")
            if _task_input(record) != inputs[task_id]:
                raise PreparationError("Public task policy differs between input and evaluator contract")
            verifiers = record.get("verifiers")
            if not isinstance(verifiers, list) or not verifiers or any(not isinstance(v, dict) for v in verifiers):
                raise PreparationError("Each training contract requires a nonempty verifier list")
            names = [verifier.get("name") for verifier in verifiers]
            if any(not isinstance(name, str) or not name for name in names) or len(set(names)) != len(names):
                raise PreparationError("Training verifier identities must be normalized and unique")
            contracts[task_id] = {
                "checks_total": len(verifiers),
                "verifier_contract_sha256": canonical_sha256(verifiers),
                "verifier_names": names,
                "task_input": inputs[task_id],
                "task_input_sha256": canonical_sha256(inputs[task_id]),
            }
    if set(contracts) != set(allowed_task_ids):
        raise PreparationError("Training contracts do not cover the frozen training membership")
    return contracts


def validate_trace(record, allowed_task_ids, source_dir, expected_contracts=None) -> tuple[dict, dict]:
    """Validate a trace against an explicitly supplied canonical training contract."""
    if not isinstance(record, dict):
        raise PreparationError("Trace must be a JSON object")
    task_id = record.get("source_task_id")
    if not isinstance(task_id, str) or task_id not in allowed_task_ids:
        raise PreparationError("Trace task is not in the frozen training split")
    expected = expected_contracts.get(task_id) if isinstance(expected_contracts, dict) else None
    if not isinstance(expected, dict):
        raise PreparationError("Frozen task input and verifier contracts are required")
    task_input = _task_input(expected.get("task_input"))
    if (task_input["task_id"] != task_id or expected.get("task_input_sha256") != canonical_sha256(task_input)
            or not SHA.fullmatch(str(expected.get("verifier_contract_sha256", "")))):
        raise PreparationError("Invalid canonical training contract identity")
    payload = model_payload(record)
    messages = payload["messages"]
    if (len(messages) < 3 or messages[0] != {"role": "system", "content": task_input["system_prompt"]}
            or messages[1] != {"role": "user", "content": task_input["user_prompt"]}
            or any(message["role"] in {"system", "user"} for message in messages[2:])):
        raise PreparationError("Trace must retain the exact canonical policy and user request without added instructions")
    visible_names = {tool["function"]["name"] for tool in payload["tools"]}
    if visible_names != set(task_input["selected_tools"]):
        raise PreparationError("Visible tool-name set differs from canonical selected_tools")
    review = record.get("review")
    if not isinstance(review, dict) or review.get("status") != "accepted":
        raise PreparationError("Every trace needs an externally supplied accepted review")
    _nonempty(review.get("reviewer"), "reviewer")
    reviewed_at = _nonempty(review.get("reviewed_at"), "reviewed_at")
    try:
        when = datetime.fromisoformat(reviewed_at.replace("Z", "+00:00"))
        if when.tzinfo is None:
            raise ValueError("timezone missing")
    except ValueError as error:
        raise PreparationError("reviewed_at must be an ISO timestamp with timezone") from error
    if review.get("no_evaluation_or_privileged_content") is not True:
        raise PreparationError("Review must explicitly attest to model-visible content isolation")
    if review.get("model_visible_sha256") != canonical_sha256(payload):
        raise PreparationError("Reviewed model-visible payload hash mismatch")
    if review.get("task_input_sha256") != expected["task_input_sha256"]:
        raise PreparationError("Review is not bound to the canonical task input")
    provenance = record.get("provenance")
    keys = ("teacher_model", "generator_revision", "environment_revision", "source_trace_id")
    if not isinstance(provenance, dict):
        raise PreparationError("Trace provenance is required")
    for key in keys:
        _nonempty(provenance.get(key), f"provenance.{key}")
    receipt_ref = review.get("verifier_receipt")
    if not isinstance(receipt_ref, dict) or not SHA.fullmatch(str(receipt_ref.get("sha256", ""))):
        raise PreparationError("Review requires a verifier receipt file and its SHA256")
    receipt_path = Path(_nonempty(receipt_ref.get("path"), "verifier receipt path"))
    if not receipt_path.is_absolute():
        receipt_path = Path(source_dir) / receipt_path
    if not receipt_path.is_file() or receipt_path.stat().st_size > 10 * 1024**2:
        raise PreparationError("Verifier receipt is missing or too large")
    if sha256_file(receipt_path) != receipt_ref["sha256"]:
        raise PreparationError("Verifier receipt hash mismatch")
    try:
        receipt = _json_loads(receipt_path.read_text())
    except (OSError, ValueError) as error:
        raise PreparationError("Verifier receipt must be a JSON object") from error
    if not isinstance(receipt, dict):
        raise PreparationError("Verifier receipt must be a JSON object")
    if type(receipt.get("schema_version")) is not int or receipt["schema_version"] != RECEIPT_SCHEMA_VERSION:
        raise PreparationError("Receipt schema version 2 requires canonical input binding and indexed outcomes")
    count = receipt.get("checks_total")
    if (receipt.get("source_task_id") != task_id or receipt.get("status") != "passed" or
            isinstance(count, bool) or not isinstance(count, int) or count <= 0 or
            type(receipt.get("checks_passed")) is not int or receipt.get("checks_passed") != count):
        raise PreparationError("Receipt must report all nonempty checks passed for this task")
    if receipt.get("model_visible_sha256") != review["model_visible_sha256"]:
        raise PreparationError("Verifier receipt is not bound to this reviewed trace")
    if receipt.get("task_input_sha256") != expected["task_input_sha256"]:
        raise PreparationError("Verifier receipt is not bound to the canonical task input")
    if count != expected.get("checks_total"):
        raise PreparationError("Receipt does not cover the full required verifier count")
    if receipt.get("verifier_contract_sha256") != expected.get("verifier_contract_sha256"):
        raise PreparationError("Receipt verifier contract hash differs from the frozen working contract")
    outcomes = receipt.get("outcomes")
    verifier_names = expected.get("verifier_names")
    if (not isinstance(verifier_names, list) or len(verifier_names) != count
            or not isinstance(outcomes, list) or len(outcomes) != count):
        raise PreparationError("Receipt requires exactly one indexed outcome per required verifier")
    seen_outcomes = set()
    for outcome in outcomes:
        if not isinstance(outcome, dict):
            raise PreparationError("Verifier outcomes must be objects")
        index = outcome.get("verifier_index")
        if type(index) is not int or not 0 <= index < count or index in seen_outcomes:
            raise PreparationError("Invalid or duplicate verifier outcome index")
        if outcome.get("verifier_name") != verifier_names[index]:
            raise PreparationError("Verifier outcome name does not match its normalized index")
        if outcome.get("passed") is not True or outcome.get("error") not in (None, ""):
            raise PreparationError("Every required verifier outcome must pass without an error")
        seen_outcomes.add(index)
    _nonempty(receipt.get("verifier_revision"), "verifier revision")
    attestation = {
        "reviewer": review["reviewer"], "reviewed_at": reviewed_at,
        "model_visible_sha256": review["model_visible_sha256"],
        "task_input_sha256": expected["task_input_sha256"],
        "verifier_receipt_sha256": receipt_ref["sha256"],
        "verifier_revision": receipt["verifier_revision"], "checks_total": count,
        "verifier_contract_sha256": receipt.get("verifier_contract_sha256"),
        "verifier_outcomes_sha256": canonical_sha256(outcomes),
        "receipt_schema_version": RECEIPT_SCHEMA_VERSION,
        "provenance": {key: provenance[key] for key in keys},
    }
    return {"source_task_id": task_id, **payload}, attestation


def read_reviewed_traces(source_path, split_manifest_path,
                         training_contracts_path=TRAINING_CONTRACTS_PATH,
                         expected_contracts=None,
                         task_inputs_path=TRAINING_INPUTS_PATH) -> tuple[list, dict, dict]:
    source, split_path = Path(source_path), Path(split_manifest_path)
    split = _json_loads(split_path.read_text())
    ids = split.get("task_ids", {}).get("train", [])
    if len(ids) != 128 or len(set(ids)) != 128 or split.get("counts", {}).get("train") != 128:
        raise PreparationError("Expected the frozen 128-task training membership")
    others = set(split["task_ids"].get("development", [])) | set(split["task_ids"].get("final_test", []))
    if set(ids) & others:
        raise PreparationError("Frozen split has overlapping training/evaluation membership")
    if expected_contracts is None:
        expected_contracts = load_training_contracts(training_contracts_path, set(ids), task_inputs_path)
    if set(expected_contracts) != set(ids):
        raise PreparationError("Expected verifier contracts must cover all frozen training tasks")
    traces, receipts, seen = [], {}, set()
    with source.open() as handle:
        for number, line in enumerate(handle, 1):
            if not line.strip():
                continue
            try:
                trace, receipt = validate_trace(_json_loads(line), set(ids), source.parent, expected_contracts)
            except (ValueError, OSError) as error:
                raise PreparationError(f"Trace line {number}: {error}") from error
            task_id = trace["source_task_id"]
            if task_id in seen:
                raise PreparationError("Expected one complete reviewed trajectory per training task")
            seen.add(task_id)
            traces.append(trace)
            receipts[task_id] = receipt
    if seen != set(ids):
        raise PreparationError(f"Missing reviewed training workflows: {len(set(ids) - seen)} of 128")
    return sorted(traces, key=lambda trace: trace["source_task_id"]), receipts, split


def tokenize_trace(trace, tokenizer, template, max_seq_length) -> dict:
    """Assert rendering/prefix equivalence and independently audit assistant masks."""
    messages, tools = trace["messages"], trace["tools"]
    kwargs = {"tools": tools, "enable_thinking": True, "add_generation_prompt": False}
    def render(subset, chosen=template, generation=False):
        return tokenizer.apply_chat_template(subset, chat_template=chosen, tools=tools,
                                             enable_thinking=True, add_generation_prompt=generation,
                                             tokenize=False)
    original = tokenizer.chat_template
    if not isinstance(original, str) or not original:
        raise PreparationError("Pinned tokenizer lacks its original chat template")
    rendered = render(messages)
    if rendered != render(messages, original):
        raise PreparationError("Training template changes original model rendering; trace needs review")
    encoded = tokenizer.apply_chat_template(messages, chat_template=template, tokenize=True,
                                             return_dict=True, return_assistant_tokens_mask=True,
                                             truncation=False, **kwargs)
    ids, mask = encoded.get("input_ids"), encoded.get("assistant_masks")
    if (not isinstance(ids, list) or not isinstance(mask, list) or not ids or len(ids) != len(mask)
            or any(type(value) is not int or value < 0 for value in ids)
            or any(value not in (0, 1) for value in mask)):
        raise PreparationError("Tokenizer did not return valid IDs and assistant masks")
    if len(ids) > max_seq_length:
        raise PreparationError(f"Complete trace has {len(ids)} tokens > cap {max_seq_length}; never truncated")
    explicit = tokenizer(rendered, add_special_tokens=False, return_offsets_mapping=True)
    if explicit["input_ids"] != ids:
        raise PreparationError("Rendered-text tokenization differs from chat tokenization")
    spans = []
    for index, message in enumerate(messages):
        if message["role"] != "assistant":
            continue
        before, after = render(messages[:index]), render(messages[:index + 1])
        header = "<|im_start|>assistant\n"
        if not after.startswith(before + header) or not rendered.startswith(after):
            raise PreparationError("Assistant serialization is not prefix-preserving")
        if after != render(messages[:index + 1], original):
            raise PreparationError("Training and original template prefixes disagree")
        prompt = render(messages[:index], original, generation=True)
        if not rendered.startswith(prompt):
            raise PreparationError("Original generation prompt does not match the supervised prefix")
        spans.append((len(before) + len(header), len(after)))
    offsets = explicit.get("offset_mapping", [])
    if len(offsets) != len(ids):
        raise PreparationError("A fast tokenizer with complete offsets is required")
    expected = [int(any(start < right and end > left for left, right in spans))
                for start, end in offsets]
    if expected != mask:
        raise PreparationError("Assistant mask misses targets or supervises a non-assistant token")
    for left, right in spans:
        if not any(mask[index] and start < right and end > left
                   for index, (start, end) in enumerate(offsets)):
            raise PreparationError("An assistant turn has no supervised tokens")
    if mask[0] or not any(mask[1:]):
        raise PreparationError("First token must be masked and shifted labels must be nonempty")
    return {"input_ids": ids, "labels": [token if enabled else -100 for token, enabled in zip(ids, mask)],
            "source_task_id": trace["source_task_id"]}


def validate_local_tokenizer(tokenizer_dir=TOKENIZER_DIRECTORY, model_revision=MODEL_REVISION) -> tuple[Path, dict]:
    """Require pinned, hashed local assets; never discover a home cache or download."""
    directory = Path(tokenizer_dir).resolve()
    root = ROOT.resolve()
    if not directory.is_relative_to(root) or not directory.is_dir():
        raise PreparationError("Tokenizer assets must exist inside this workspace; no download/cache fallback is permitted")
    manifest_path = directory.parent / "manifest.json"
    if manifest_path.is_symlink() or not manifest_path.is_file():
        raise PreparationError("Local tokenizer needs a neighboring manifest.json with pinned file hashes")
    manifest = _json_loads(manifest_path.read_text())
    if (not isinstance(manifest, dict) or manifest.get("model_id") != MODEL_ID
            or manifest.get("model_revision") != model_revision
            or manifest.get("tokenizer_revision") != model_revision):
        raise PreparationError("Local tokenizer model/revision differs from the requested pinned identity")
    local_path = manifest.get("local_model_path")
    if not isinstance(local_path, str) or (root / local_path).resolve() != directory:
        raise PreparationError("Tokenizer manifest local_model_path differs from the selected directory")
    if manifest.get("versions") != EXPECTED_VERSIONS:
        raise PreparationError("Tokenizer manifest versions differ from the reviewed tokenizer stack")
    required = {"tokenizer.json", "tokenizer_config.json", "chat_template.jinja"}
    entries = manifest.get("files")
    if not isinstance(entries, dict) or set(entries) != required:
        raise PreparationError("Tokenizer manifest must describe exactly the three reviewed assets")
    if {path.name for path in directory.iterdir()} != required:
        raise PreparationError("Tokenizer directory contains missing or unreviewed extra assets")
    for name, entry in entries.items():
        path = directory / name
        if path.is_symlink() or not path.is_file() or not isinstance(entry, dict):
            raise PreparationError("Tokenizer assets must be ordinary local files")
        expected_url = f"https://huggingface.co/{MODEL_ID}/resolve/{model_revision}/{name}"
        if (entry.get("url") != expected_url or not SHA.fullmatch(str(entry.get("sha256", "")))
                or type(entry.get("bytes")) is not int or entry["bytes"] <= 0):
            raise PreparationError("Tokenizer asset manifest lacks valid immutable provenance")
        if path.stat().st_size != entry["bytes"] or sha256_file(path) != entry["sha256"]:
            raise PreparationError(f"Local tokenizer asset hash/size mismatch: {name}")
    return directory, manifest


def prepare_dataset(source_path, split_manifest_path, output_dir, *, max_seq_length=16384,
                    model_revision=MODEL_REVISION,
                    training_contracts_path=TRAINING_CONTRACTS_PATH,
                    task_inputs_path=TRAINING_INPUTS_PATH,
                    tokenizer_dir=TOKENIZER_DIRECTORY) -> dict:
    if not re.fullmatch(r"[0-9a-f]{40}", model_revision):
        raise PreparationError("Use an immutable model revision")
    if not 1 <= max_seq_length <= 32768:
        raise PreparationError("This campaign supports a maximum of 32768 tokens")
    contracts_sha256 = sha256_file(training_contracts_path)
    inputs_sha256 = sha256_file(task_inputs_path)
    traces_sha256 = sha256_file(source_path)
    split_sha256 = sha256_file(split_manifest_path)
    traces, receipts, split = read_reviewed_traces(source_path, split_manifest_path, training_contracts_path,
                                                 task_inputs_path=task_inputs_path)
    if (contracts_sha256 != sha256_file(training_contracts_path)
            or inputs_sha256 != sha256_file(task_inputs_path)
            or traces_sha256 != sha256_file(source_path)
            or split_sha256 != sha256_file(split_manifest_path)):
        raise PreparationError("Training inputs, contracts, traces or membership changed during review validation")
    versions = {name: importlib.metadata.version(name) for name in EXPECTED_VERSIONS}
    if versions != EXPECTED_VERSIONS:
        raise PreparationError(f"Tokenizer environment must match pinned versions: {EXPECTED_VERSIONS}; found {versions}")
    local_tokenizer, tokenizer_manifest = validate_local_tokenizer(tokenizer_dir, model_revision)
    tokenizer_manifest_sha256 = sha256_file(local_tokenizer.parent / "manifest.json")
    from transformers import AutoTokenizer
    tokenizer = AutoTokenizer.from_pretrained(str(local_tokenizer), trust_remote_code=False, use_fast=True,
                                              local_files_only=True, token=False,
                                              cache_dir=str(ROOT / "work" / "tokenizer-cache"))
    if not tokenizer.is_fast:
        raise PreparationError("Fast tokenizer required for offset/mask verification")
    if sha256_file(TEMPLATE_PATH) != TEMPLATE_SHA256:
        raise PreparationError("Bundled reviewed training template hash changed")
    template = TEMPLATE_PATH.read_text()
    destination = Path(output_dir)
    if destination.exists():
        raise PreparationError("Refusing to overwrite an existing prepared dataset")
    destination.parent.mkdir(parents=True, exist_ok=True)
    staging = Path(tempfile.mkdtemp(prefix=".prepare-sft-", dir=destination.parent))
    try:
        total_tokens = supervised = 0
        token_file = staging / "train.tokens.jsonl"
        with token_file.open("w") as handle:
            for trace in traces:
                row = tokenize_trace(trace, tokenizer, template, max_seq_length)
                handle.write(json.dumps(row, separators=(",", ":"), allow_nan=False) + "\n")
                total_tokens += len(row["input_ids"])
                supervised += sum(label != -100 for label in row["labels"])
        shutil.copyfile(TEMPLATE_PATH, staging / "training_chat_template.jinja")
        manifest = {
            "schema_version": 1, "status": "READY_FOR_TRAINING", "ready": True,
            "created_utc": datetime.now(timezone.utc).isoformat(),
            "model_id": MODEL_ID, "model_revision": model_revision,
            "tokenizer_revision": model_revision, "max_seq_length": max_seq_length,
            "train_file": token_file.name, "train_file_sha256": sha256_file(token_file),
            "split_manifest_sha256": split_sha256,
            "training_contracts_sha256": contracts_sha256,
            "training_inputs_sha256": inputs_sha256,
            "receipt_schema_version": RECEIPT_SCHEMA_VERSION,
            "source_traces_sha256": traces_sha256,
            "local_tokenizer_manifest_sha256": tokenizer_manifest_sha256,
            "tokenizer_asset_sha256": {name: entry["sha256"] for name, entry in tokenizer_manifest["files"].items()},
            "chat_template_file": "training_chat_template.jinja",
            "chat_template_sha256": sha256_file(TEMPLATE_PATH), "chat_template_source": TEMPLATE_SOURCE,
            "original_chat_template_sha256": hashlib.sha256(tokenizer.chat_template.encode()).hexdigest(),
            "training_task_ids": sorted(split["task_ids"]["train"]),
            "task_count": len(traces), "row_count": len(traces),
            "total_tokens": total_tokens, "supervised_tokens": supervised,
            "versions": versions, "review_receipts": receipts,
            "review_scope": "External accepted review/receipt assertions validated for identity and hashes; verifier not independently executed by this preparer.",
            "label_policy": "All assistant targets once; non-assistant/header tokens masked; original rendering and generation-prefix equivalence checked; no truncation.",
        }
        if (contracts_sha256 != sha256_file(training_contracts_path)
                or inputs_sha256 != sha256_file(task_inputs_path)
                or traces_sha256 != sha256_file(source_path)
                or split_sha256 != sha256_file(split_manifest_path)):
            raise PreparationError("Training inputs, contracts, traces or membership changed during dataset preparation")
        validate_local_tokenizer(local_tokenizer, model_revision)
        if tokenizer_manifest_sha256 != sha256_file(local_tokenizer.parent / "manifest.json"):
            raise PreparationError("Tokenizer provenance changed during dataset preparation")
        (staging / "prepared_manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")
        staging.rename(destination)
        return manifest
    finally:
        if staging.exists():
            shutil.rmtree(staging)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--traces", required=True, type=Path)
    parser.add_argument("--split-manifest", type=Path, default=ROOT / "data/metadata/split_manifest.json")
    parser.add_argument("--training-contracts", type=Path, default=TRAINING_CONTRACTS_PATH,
                        help="Working normalized training verifier contracts only; never held-out contracts")
    parser.add_argument("--training-inputs", type=Path, default=TRAINING_INPUTS_PATH,
                        help="Canonical public training questions, policies and selected tool names")
    parser.add_argument("--tokenizer-dir", type=Path, default=TOKENIZER_DIRECTORY,
                        help="Verified local tokenizer directory inside this workspace; never downloads or uses a home cache")
    parser.add_argument("--output-dir", type=Path)
    parser.add_argument("--max-seq-length", type=int, default=16384)
    parser.add_argument("--model-revision", default=MODEL_REVISION)
    parser.add_argument("--validate-only", action="store_true")
    args = parser.parse_args()
    try:
        if args.validate_only:
            traces, _, _ = read_reviewed_traces(args.traces, args.split_manifest, args.training_contracts,
                                              task_inputs_path=args.training_inputs)
            print(json.dumps({"reviewed_workflows": len(traces), "tokenized": False,
                              "ready_for_training": False, "verifier_independently_executed": False}))
        else:
            if args.output_dir is None:
                parser.error("--output-dir is required unless --validate-only is set")
            manifest = prepare_dataset(args.traces, args.split_manifest, args.output_dir,
                                       max_seq_length=args.max_seq_length, model_revision=args.model_revision,
                                       training_contracts_path=args.training_contracts,
                                       task_inputs_path=args.training_inputs,
                                       tokenizer_dir=args.tokenizer_dir)
            print(json.dumps({key: manifest[key] for key in ("status", "task_count", "total_tokens", "supervised_tokens", "train_file_sha256")}))
    except (PreparationError, OSError, ValueError, importlib.metadata.PackageNotFoundError) as error:
        parser.exit(2, f"Preparation refused: {error}\n")


if __name__ == "__main__":
    main()
