import copy
from contextlib import contextmanager
import hashlib
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import importlib.util
import json
from pathlib import Path
import tempfile
import threading
import unittest
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "local_collection_harness", ROOT / "scripts/local_collection_harness.py"
)
harness = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(harness)


LOOKUP_TOOL = {
    "type": "function",
    "function": {
        "name": "lookup_record",
        "description": "Native lookup description from the live test catalog.",
        "parameters": {
            "type": "object",
            "properties": {"query": {"type": "string"}},
            "required": ["query"],
            "additionalProperties": False,
        },
    },
}
UPDATE_TOOL = {
    "type": "function",
    "function": {
        "name": "update_record",
        "description": "Native update description from the live test catalog.",
        "parameters": {
            "type": "object",
            "properties": {
                "record_id": {"type": "string"},
                "value": {"type": "string"},
            },
            "required": ["record_id", "value"],
            "additionalProperties": False,
        },
    },
}


def task_input():
    return {
        "task_id": "train-task",
        "domain": "itsm",
        "system_prompt": "Synthetic unit-test policy. Use only observed records.",
        "user_prompt": "Find the synthetic record and update it.",
        "selected_tools": ["lookup_record", "update_record"],
        "restricted_tools": [],
    }


def verifiers():
    return [
        {
            "verifier_type": "database_state",
            "name": "check-0000: update exists",
            "gym_name": "gym-itsm-mcp",
            "validation_config": {
                "query": "SELECT 1 AS updated",
                "expected_value": 1,
                "comparison_type": "equals",
            },
        },
        {
            "verifier_type": "database_state",
            "name": "check-0001: no duplicate",
            "gym_name": "gym-itsm-mcp",
            "validation_config": {
                "query": "SELECT 0 AS duplicate_count",
                "expected_value": 0,
                "comparison_type": "equals",
            },
        },
    ]


def bundle():
    public_input = task_input()
    checks = verifiers()
    return {
        "task_input": public_input,
        "verifiers": checks,
        "task_input_sha256": harness.canonical_sha256(public_input),
        "verifier_contract_sha256": harness.canonical_sha256(checks),
        "generator_revision": "synthetic-generator-revision",
        "environment_revision": "synthetic-environment-revision",
        "verifier_revision": "synthetic-verifier-revision",
    }


def accepted_review():
    return {
        "status": "accepted",
        "reviewer": "independent-unit-test-reviewer",
        "reviewed_at": "2026-09-15T12:00:00Z",
        "no_evaluation_or_privileged_content": True,
    }


def passing_outcomes():
    return [
        {
            "verifier_index": 0,
            "verifier_name": "check-0000: update exists",
            "passed": True,
            "error": None,
        },
        {
            "verifier_index": 1,
            "verifier_name": "check-0001: no duplicate",
            "passed": True,
            "error": None,
        },
    ]


def pending_attempt(*, usage=None):
    tools = [copy.deepcopy(LOOKUP_TOOL), copy.deepcopy(UPDATE_TOOL)]
    messages = [
        {"role": "system", "content": task_input()["system_prompt"]},
        {"role": "user", "content": task_input()["user_prompt"]},
        {
            "role": "assistant",
            "content": "",
            "tool_calls": [
                {
                    "id": "call-1",
                    "type": "function",
                    "function": {
                        "name": "lookup_record",
                        "arguments": {"query": "synthetic"},
                    },
                }
            ],
        },
        {
            "role": "tool",
            "tool_call_id": "call-1",
            "name": "lookup_record",
            "content": json.dumps({"record_id": "observed-1"}, sort_keys=True),
        },
        {"role": "assistant", "content": "The observed record was updated."},
    ]
    return {
        "attempt_id": "attempt-unit-test",
        "source_task_id": "train-task",
        "status": "RECORDED_PENDING_REVIEW",
        "messages": messages,
        "tools": tools,
        "usage": usage,
        "cleanup_success": True,
        "execution_evidence": {
            "event_log_head_sha256": "b" * 64,
            "integrity_scope": "synthetic-unit-test",
        },
        "provenance": {
            "teacher_model": "synthetic-solver-not-a-teacher",
            "generator_revision": "synthetic-generator-revision",
            "environment_revision": "synthetic-environment-revision",
            "source_trace_id": "attempt-unit-test",
        },
    }


class FakeSolver:
    def __init__(self, responses):
        self.responses = list(responses)
        self.invocations = []

    def invoke(self, messages, tools):
        self.invocations.append(
            {"messages": copy.deepcopy(messages), "tools": copy.deepcopy(tools)}
        )
        if not self.responses:
            raise AssertionError("solver invoked more times than expected")
        response = self.responses.pop(0)
        if isinstance(response, BaseException):
            raise response
        return copy.deepcopy(response)


class FakeRuntime:
    def __init__(self, tools=None, *, fail_cleanup=False, fail_sql=None):
        self.tools = copy.deepcopy(
            [LOOKUP_TOOL, UPDATE_TOOL] if tools is None else tools
        )
        self.fail_cleanup = fail_cleanup
        self.fail_sql = fail_sql
        self.seed_attempt_ids = []
        self.database_ids = []
        self.discover_requests = []
        self.tool_calls = []
        self.sql_calls = []
        self.cleanup_calls = 0

    def seed_all(self, attempt_id):
        self.seed_attempt_ids.append(attempt_id)
        databases = {"gym-itsm-mcp": f"db-{attempt_id}-itsm"}
        self.database_ids.append(databases)
        return databases

    def discover_selected_tools(self, selected_names):
        self.discover_requests.append(list(selected_names))
        routing = {name: "gym-itsm-mcp" for name in selected_names}
        return (
            copy.deepcopy(self.tools),
            routing,
            harness.canonical_sha256(self.tools),
            {"selected_tools": copy.deepcopy(self.tools), "routing": routing},
        )

    def call_tool(self, name, args):
        self.tool_calls.append((name, copy.deepcopy(args)))
        if name == "lookup_record":
            return {"result": {"record_id": "observed-1"}, "raw_response": "{}", "transport": {}}
        if name == "update_record":
            return {"result": {"updated": True}, "raw_response": "{}", "transport": {}}
        raise AssertionError(f"unexpected tool call: {name}")

    def run_sql(self, gym_name, query):
        self.sql_calls.append((gym_name, query))
        if self.fail_sql and self.fail_sql in query:
            raise RuntimeError("synthetic verifier transport failure")
        if "duplicate_count" in query:
            return {"result": {"data": [{"duplicate_count": 0}]}, "raw_response": "{}", "transport": {}}
        return {"result": {"data": [{"updated": 1}]}, "raw_response": "{}", "transport": {}}

    def cleanup(self):
        self.cleanup_calls += 1
        if self.fail_cleanup:
            raise RuntimeError("synthetic cleanup failure")


def assistant_tool_call():
    return {
        "role": "assistant",
        "content": "",
        "tool_calls": [
            {
                "id": "call-1",
                "type": "function",
                "function": {
                    "name": "lookup_record",
                    "arguments": {"query": "synthetic"},
                },
            }
        ],
    }


def assistant_final():
    return {
        "role": "assistant",
        "content": "The observed record was updated.",
        "usage": None,
    }


class LoopbackMCPHandler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"
    requests = []
    wrong_id = False
    invalid_json_paths = set()

    def log_message(self, format, *args):
        return

    def _reply(self, status, payload=None, *, session=None, content_type="application/json"):
        body = b"" if payload is None else json.dumps(payload).encode("utf-8")
        self.send_response(status)
        if body:
            self.send_header("Content-Type", content_type)
        if session:
            self.send_header("Mcp-Session-Id", session)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        if body:
            self.wfile.write(body)

    def do_POST(self):
        length = int(self.headers.get("Content-Length", "0"))
        raw = self.rfile.read(length)
        type(self).requests.append((self.path, dict(self.headers), raw))
        if self.path in type(self).invalid_json_paths:
            body = b"not-json"
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return
        request = json.loads(raw)
        method = request.get("method")
        if method == "notifications/initialized":
            self._reply(204)
            return
        request_id = "wrong" if type(self).wrong_id else request["id"]
        if method == "initialize":
            result = {"protocolVersion": "2024-11-05", "capabilities": {"tools": {}}}
            self._reply(200, {"jsonrpc": "2.0", "id": request_id, "result": result}, session="session-1")
        elif method == "tools/list":
            if self.headers.get("Mcp-Session-Id") != "session-1":
                self._reply(400, {"error": "missing session"})
                return
            self._reply(200, {"jsonrpc": "2.0", "id": request_id, "result": {"tools": [{"name": "lookup_record", "description": "live", "inputSchema": LOOKUP_TOOL["function"]["parameters"]}]}})
        elif method == "tools/call":
            self._reply(200, {"jsonrpc": "2.0", "id": request_id, "result": {"isError": True, "content": [{"type": "text", "text": "synthetic failure"}]}})
        else:
            self._reply(200, {"jsonrpc": "2.0", "id": request_id, "result": {}})


@contextmanager
def loopback_server():
    LoopbackMCPHandler.requests = []
    LoopbackMCPHandler.wrong_id = False
    LoopbackMCPHandler.invalid_json_paths = set()
    server = ThreadingHTTPServer(("127.0.0.1", 0), LoopbackMCPHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield server
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=2)


def runtime_for_port(port):
    runtime_bundle = bundle()
    runtime_bundle["gym_servers_config"] = [
        {
            "mcp_server_name": "gym-itsm-mcp",
            "seed_database_file": "unused.sql",
            "context": {},
        }
    ]
    runtime_bundle["mcp_endpoint"] = "/mcp"
    runtime = harness.HTTPTaskRuntime(
        runtime_bundle,
        attempt_id="attempt-loopback",
        databases={"gym-itsm-mcp": "db-loopback"},
    )
    runtime.environment = {
        "servers": {
            "gym-itsm-mcp": {
                "url": f"http://127.0.0.1:{port}",
                "container_port": port,
                "image": "example.invalid/test@sha256:" + "a" * 64,
            }
        }
    }
    return runtime


class CanonicalAndVerifierHelperTests(unittest.TestCase):
    def test_canonical_hash_is_stable_utf8_and_rejects_nan(self):
        value = {"z": "café", "a": [2, 1]}
        expected = hashlib.sha256(
            '{"a":[2,1],"z":"café"}'.encode("utf-8")
        ).hexdigest()
        self.assertEqual(harness.canonical_sha256(value), expected)
        self.assertEqual(
            harness.canonical_sha256(value),
            harness.canonical_sha256({"a": [2, 1], "z": "café"}),
        )
        with self.assertRaises((TypeError, ValueError)):
            harness.canonical_sha256({"not_a_number": float("nan")})

    def test_extract_sql_value_accepts_observed_single_scalar_shapes(self):
        self.assertEqual(harness.extract_sql_value({"data": [{"count": 1}]}), 1)
        self.assertEqual(harness.extract_sql_value({"rows": [[0]]}), 0)
        self.assertEqual(harness.extract_sql_value({"rows": [{"count": 2}]}), 2)

    def test_extract_sql_value_preserves_nonscalar_observations(self):
        self.assertEqual(harness.extract_sql_value({"data": []}), [])
        self.assertEqual(harness.extract_sql_value({"rows": []}), [])
        self.assertEqual(
            harness.extract_sql_value({"data": [{"a": 1, "b": 2}]}),
            {"a": 1, "b": 2},
        )
        self.assertEqual(
            harness.extract_sql_value({"rows": [{"a": 1}, {"a": 2}]}),
            [{"a": 1}, {"a": 2}],
        )

    def test_compare_values_is_fail_closed(self):
        self.assertTrue(harness.compare_values(1, 1, "equals"))
        self.assertTrue(harness.compare_values(2, 1, "greater_than"))
        self.assertTrue(harness.compare_values(0, 1, "less_than"))
        self.assertTrue(harness.compare_values("observed value", "value", "contains"))
        self.assertFalse(harness.compare_values(0, 1, "equals"))
        self.assertFalse(harness.compare_values(1, 1, "unknown-comparison"))

    def test_executor_metadata_redaction_is_exact_recursive_and_lossless_elsewhere(self):
        database_id = "db_1234567890_secret"
        token = "token-secret-value"
        value = {
            "etag": f"etag-{database_id}",
            "nested": [{"token_echo": token, "business_id": "case-123"}],
            "number": 7,
        }
        cleaned, count = harness._redact_executor_metadata(value, [database_id, token])
        self.assertEqual(count, 2)
        self.assertEqual(cleaned["etag"], "etag-[REDACTED_EXECUTOR_METADATA]")
        self.assertEqual(cleaned["nested"][0]["token_echo"], "[REDACTED_EXECUTOR_METADATA]")
        self.assertEqual(cleaned["nested"][0]["business_id"], "case-123")
        self.assertEqual(cleaned["number"], 7)
        self.assertEqual(value["etag"], f"etag-{database_id}")


class RuntimeContextHeaderTests(unittest.TestCase):
    def _runtime(self, gym_name, context):
        runtime_bundle = bundle()
        runtime_bundle["gym_servers_config"] = [
            {
                "mcp_server_name": gym_name,
                "seed_database_file": "unused.sql",
                "context": context,
            }
        ]
        return harness.HTTPTaskRuntime(runtime_bundle, attempt_id="attempt-header-test")

    def test_calendar_token_header_alias_is_normalized_without_changing_value(self):
        runtime = self._runtime("gym-calendar", {"x-hr-user-token": "opaque-calendar-token"})
        headers = runtime._headers("gym-calendar", include_database=False)
        self.assertEqual(headers, {"x-access-token": "opaque-calendar-token"})
        self.assertEqual(
            runtime.context_header_normalizations,
            {
                "gym-calendar": [
                    {
                        "source_header": "x-hr-user-token",
                        "target_header": "x-access-token",
                    }
                ]
            },
        )

    def test_hr_token_header_alias_is_normalized_without_changing_value(self):
        runtime = self._runtime("sn-hr-internal", {"x-access-token": "opaque-hr-token"})
        headers = runtime._headers("sn-hr-internal", include_database=False)
        self.assertEqual(headers, {"x-hr-user-token": "opaque-hr-token"})

    def test_ambiguous_alias_and_canonical_header_fails_closed(self):
        runtime = self._runtime(
            "gym-calendar",
            {"x-hr-user-token": "one", "x-access-token": "two"},
        )
        with self.assertRaisesRegex(ValueError, "Ambiguous authentication context"):
            runtime._headers("gym-calendar", include_database=False)


class SolverValidationTests(unittest.TestCase):
    def test_exact_selected_schema_set_is_required_and_preserved(self):
        schemas = [copy.deepcopy(LOOKUP_TOOL), copy.deepcopy(UPDATE_TOOL)]
        response = assistant_tool_call()
        validated = harness.validate_solver_response(
            response,
            schemas,
            selected_tool_names=["lookup_record", "update_record"],
        )
        self.assertEqual(validated, response)
        self.assertEqual(schemas[0]["function"]["description"], LOOKUP_TOOL["function"]["description"])

        with self.assertRaises((TypeError, ValueError)):
            harness.validate_solver_response(
                response,
                schemas[:1],
                selected_tool_names=["lookup_record", "update_record"],
            )

    def test_reasoning_usage_and_argument_names_are_strict(self):
        response = assistant_tool_call()
        response["reasoning_content"] = {"not": "text"}
        with self.assertRaises(ValueError):
            harness.validate_solver_response(response, [LOOKUP_TOOL, UPDATE_TOOL])
        response = assistant_tool_call()
        response["tool_calls"][0]["function"]["arguments"] = {"unsafe/key": "x"}
        with self.assertRaises(ValueError):
            harness.validate_solver_response(response, [LOOKUP_TOOL, UPDATE_TOOL])


class RealLoopbackTransportTests(unittest.TestCase):
    def test_initialize_notification_session_and_iserror_are_preserved(self):
        with loopback_server() as server:
            runtime = runtime_for_port(server.server_port)
            tools, routing, digest, record = runtime.discover_selected_tools(["lookup_record"])
            self.assertEqual([tool["function"]["name"] for tool in tools], ["lookup_record"])
            self.assertEqual(routing, {"lookup_record": "gym-itsm-mcp"})
            self.assertEqual(digest, harness.canonical_sha256(record))
            self.assertEqual(runtime.session_ids, {"gym-itsm-mcp": "session-1"})
            methods = [json.loads(raw)["method"] for _, _, raw in LoopbackMCPHandler.requests]
            self.assertEqual(methods[:3], ["initialize", "notifications/initialized", "tools/list"])
            outcome = runtime.call_tool("lookup_record", {"query": "synthetic"})
            self.assertIs(outcome["result"]["isError"], True)
            self.assertEqual(outcome["transport"]["protocol"], "jsonrpc-2.0-http")

    def test_invalid_json_and_wrong_jsonrpc_id_fail_closed(self):
        with loopback_server() as server:
            runtime = runtime_for_port(server.server_port)
            LoopbackMCPHandler.invalid_json_paths = {"/mcp"}
            with self.assertRaisesRegex(RuntimeError, "Invalid JSON"):
                runtime._mcp("gym-itsm-mcp", "tools/list", {})
        with loopback_server() as server:
            runtime = runtime_for_port(server.server_port)
            LoopbackMCPHandler.wrong_id = True
            with self.assertRaisesRegex(RuntimeError, "envelope mismatch"):
                runtime._mcp("gym-itsm-mcp", "initialize", {})

    def test_loopback_origin_parser_rejects_userinfo(self):
        runtime = runtime_for_port(8000)
        runtime.environment["servers"]["gym-itsm-mcp"]["url"] = "http://localhost:8000@remote.invalid"
        with self.assertRaises(ValueError):
            runtime._base("gym-itsm-mcp")


class IntegrityEnvelopeTests(unittest.TestCase):
    def test_hash_chained_log_detects_rewrite(self):
        with tempfile.TemporaryDirectory() as temporary:
            log = harness.AppendOnlyAttemptLog(Path(temporary) / "attempt", create=True)
            log.append({"event_type": "one"})
            log.append({"event_type": "two"})
            text = log.path.read_text()
            log.path.write_text(text.replace('"event_type":"one"', '"event_type":"tampered"'))
            with self.assertRaisesRegex(ValueError, "digest mismatch"):
                log.read()

    def test_state_integrity_rejects_mutation(self):
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "state.json"
            state = {"status": "IN_PROGRESS"}
            harness._write_state(path, state)
            loaded = json.loads(path.read_text())
            loaded["status"] = "ACCEPTED"
            with self.assertRaisesRegex(ValueError, "integrity hash mismatch"):
                harness._validate_state_integrity(loaded)

    def test_parser_exposes_only_exact_step_not_legacy_call_or_finish(self):
        parser = harness.build_parser()
        subparsers = next(action for action in parser._actions if action.dest == "command")
        self.assertIn("step", subparsers.choices)
        self.assertNotIn("call", subparsers.choices)
        self.assertNotIn("finish", subparsers.choices)

    def test_duplicate_schema_names_and_unselected_calls_are_rejected(self):
        duplicate = [copy.deepcopy(LOOKUP_TOOL), copy.deepcopy(LOOKUP_TOOL)]
        with self.assertRaises((TypeError, ValueError)):
            harness.validate_solver_response(
                assistant_tool_call(),
                duplicate,
                selected_tool_names=["lookup_record", "update_record"],
            )

        response = assistant_tool_call()
        response["tool_calls"][0]["function"]["name"] = "hidden_admin_tool"
        with self.assertRaises((TypeError, ValueError)):
            harness.validate_solver_response(
                response,
                [LOOKUP_TOOL, UPDATE_TOOL],
                selected_tool_names=["lookup_record", "update_record"],
            )

    def test_call_ids_are_unique_and_not_already_pending(self):
        response = assistant_tool_call()
        response["tool_calls"].append(copy.deepcopy(response["tool_calls"][0]))
        with self.assertRaises((TypeError, ValueError)):
            harness.validate_solver_response(
                response,
                [LOOKUP_TOOL, UPDATE_TOOL],
                selected_tool_names=["lookup_record", "update_record"],
            )
        with self.assertRaises((TypeError, ValueError)):
            harness.validate_solver_response(
                assistant_tool_call(),
                [LOOKUP_TOOL, UPDATE_TOOL],
                pending_call_ids=("call-1",),
                selected_tool_names=["lookup_record", "update_record"],
            )


class AppendOnlyAttemptLogTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.directory = Path(self.temporary.name) / "attempt"

    def tearDown(self):
        self.temporary.cleanup()

    def test_log_reopens_without_truncating_and_appends_call_then_result(self):
        log = harness.AppendOnlyAttemptLog(self.directory, create=True)
        log.append({"event_type": "tool_call", "tool_call_id": "call-1", "arguments": {"q": "x"}})
        log.append({"event_type": "tool_result", "tool_call_id": "call-1", "result": {"id": "real-1"}})
        before = next(self.directory.glob("*.jsonl")).read_bytes()

        reopened = harness.AppendOnlyAttemptLog(self.directory, create=False)
        self.assertEqual([row["event_type"] for row in reopened.read()], ["tool_call", "tool_result"])
        reopened.append({"event_type": "attempt_finished", "status": "RECORDED_PENDING_REVIEW"})
        after = next(self.directory.glob("*.jsonl")).read_bytes()
        self.assertTrue(after.startswith(before))
        self.assertGreater(len(after), len(before))
        self.assertEqual(len(reopened.read()), 3)

    def test_create_refuses_to_replace_an_existing_attempt_log(self):
        log = harness.AppendOnlyAttemptLog(self.directory, create=True)
        log.append({"event_type": "attempt_started", "attempt_id": "one"})
        with self.assertRaises((FileExistsError, ValueError)):
            harness.AppendOnlyAttemptLog(self.directory, create=True)
        self.assertEqual(log.read()[0]["attempt_id"], "one")

    def test_log_rejects_non_object_events(self):
        log = harness.AppendOnlyAttemptLog(self.directory, create=True)
        with self.assertRaises((TypeError, ValueError)):
            log.append(["not", "an", "event"])
        self.assertEqual(log.read(), [])


class ReviewAndArtifactTests(unittest.TestCase):
    def test_review_readiness_requires_explicit_acceptance_and_every_index(self):
        outcomes = passing_outcomes()
        self.assertTrue(
            harness.review_acceptance_ready(accepted_review(), outcomes, 2)
        )
        for status in ("pending", "rejected", None):
            review = accepted_review()
            review["status"] = status
            with self.subTest(status=status):
                self.assertFalse(
                    harness.review_acceptance_ready(review, outcomes, 2)
                )

        self.assertFalse(
            harness.review_acceptance_ready(accepted_review(), outcomes[:1], 2)
        )
        duplicate = [outcomes[0], copy.deepcopy(outcomes[0])]
        self.assertFalse(
            harness.review_acceptance_ready(accepted_review(), duplicate, 2)
        )
        failed = copy.deepcopy(outcomes)
        failed[1]["passed"] = False
        self.assertFalse(
            harness.review_acceptance_ready(accepted_review(), failed, 2)
        )
        errored = copy.deepcopy(outcomes)
        errored[1]["error"] = "real verifier error"
        self.assertFalse(
            harness.review_acceptance_ready(accepted_review(), errored, 2)
        )

    def test_v2_receipt_is_built_only_after_review_and_binds_all_hashes(self):
        task_bundle = bundle()
        attempt = pending_attempt(usage=None)
        outcomes = passing_outcomes()
        receipt = harness.build_receipt(
            task_bundle, attempt, outcomes, accepted_review()
        )
        self.assertEqual(receipt["schema_version"], 2)
        self.assertEqual(receipt["source_task_id"], "train-task")
        self.assertEqual(receipt["status"], "passed")
        self.assertEqual(receipt["checks_total"], 2)
        self.assertEqual(receipt["checks_passed"], 2)
        self.assertEqual(receipt["task_input_sha256"], task_bundle["task_input_sha256"])
        self.assertEqual(
            receipt["verifier_contract_sha256"],
            task_bundle["verifier_contract_sha256"],
        )
        self.assertEqual(
            receipt["model_visible_sha256"],
            harness.canonical_sha256(
                {"messages": attempt["messages"], "tools": attempt["tools"]}
            ),
        )
        self.assertEqual(receipt["outcomes"], outcomes)

        review = accepted_review()
        review["status"] = "pending"
        with self.assertRaises((TypeError, ValueError)):
            harness.build_receipt(task_bundle, attempt, outcomes, review)
        with self.assertRaises((TypeError, ValueError)):
            harness.build_receipt(
                task_bundle, attempt, outcomes[:1], accepted_review()
            )

    def test_reviewed_trace_is_exact_and_requires_an_accepted_review(self):
        task_bundle = bundle()
        attempt = pending_attempt()
        receipt_ref = {"path": "receipts/train-task.json", "sha256": "a" * 64}
        trace = harness.build_reviewed_trace(
            task_bundle, attempt, receipt_ref, accepted_review()
        )
        self.assertEqual(trace["source_task_id"], "train-task")
        self.assertEqual(trace["messages"], attempt["messages"])
        self.assertEqual(trace["tools"], attempt["tools"])
        self.assertEqual(trace["provenance"], attempt["provenance"])
        self.assertEqual(trace["review"]["status"], "accepted")
        self.assertEqual(trace["review"]["verifier_receipt"], receipt_ref)
        self.assertEqual(
            trace["review"]["model_visible_sha256"],
            harness.canonical_sha256(
                {"messages": attempt["messages"], "tools": attempt["tools"]}
            ),
        )
        self.assertEqual(
            trace["review"]["task_input_sha256"],
            task_bundle["task_input_sha256"],
        )
        self.assertNotIn("usage", trace)
        self.assertNotIn("verifiers", trace)

        review = accepted_review()
        review["status"] = "rejected"
        with self.assertRaises((TypeError, ValueError)):
            harness.build_reviewed_trace(task_bundle, attempt, receipt_ref, review)


class LocalCollectionHarnessTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)

    def tearDown(self):
        self.temporary.cleanup()

    def make_log(self, name="attempt"):
        return harness.AppendOnlyAttemptLog(self.root / name, create=True)

    def test_run_uses_fresh_database_exact_schemas_and_append_only_call_results(self):
        solver = FakeSolver([assistant_tool_call(), assistant_final()])
        runtime = FakeRuntime()
        log = self.make_log()
        collector = harness.LocalCollectionHarness(
            bundle(),
            solver,
            runtime,
            log,
            teacher_model="synthetic-solver-not-a-teacher",
            max_iterations=5,
        )
        summary = collector.run_attempt()

        self.assertEqual(runtime.cleanup_calls, 1)
        self.assertEqual(len(runtime.seed_attempt_ids), 1)
        self.assertTrue(runtime.seed_attempt_ids[0])
        self.assertEqual(
            runtime.discover_requests,
            [["lookup_record", "update_record"]],
        )
        self.assertEqual(solver.invocations[0]["tools"], [LOOKUP_TOOL, UPDATE_TOOL])
        self.assertEqual(runtime.tool_calls, [("lookup_record", {"query": "synthetic"})])
        self.assertEqual(len(runtime.sql_calls), 2)

        events = log.read()
        event_types = [event["event_type"] for event in events]
        self.assertLess(event_types.index("tool_call"), event_types.index("tool_result"))
        self.assertEqual(event_types.count("verifier_outcome"), 2)
        verifier_events = [event for event in events if event["event_type"] == "verifier_outcome"]
        self.assertEqual([event["verifier_index"] for event in verifier_events], [0, 1])
        self.assertTrue(all(event["passed"] for event in verifier_events))
        result_event = next(event for event in events if event["event_type"] == "tool_result")
        self.assertEqual(result_event["tool_call_id"], "call-1")
        self.assertEqual(result_event["result"]["record_id"], "observed-1")
        self.assertEqual(summary["status"], "RECORDED_PENDING_REVIEW")

        second_solver = FakeSolver([assistant_final()])
        second_runtime = FakeRuntime()
        second = harness.LocalCollectionHarness(
            bundle(),
            second_solver,
            second_runtime,
            self.make_log("attempt-two"),
            teacher_model="synthetic-solver-not-a-teacher",
        ).run_attempt()
        self.assertNotEqual(summary["attempt_id"], second["attempt_id"])
        self.assertNotEqual(
            runtime.database_ids[0]["gym-itsm-mcp"],
            second_runtime.database_ids[0]["gym-itsm-mcp"],
        )

    def test_missing_or_duplicate_live_schemas_block_before_solver(self):
        for case, schemas in (
            ("missing", [LOOKUP_TOOL]),
            ("duplicate", [LOOKUP_TOOL, copy.deepcopy(LOOKUP_TOOL)]),
        ):
            with self.subTest(case=case):
                solver = FakeSolver([assistant_final()])
                runtime = FakeRuntime(schemas)
                log = self.make_log(f"blocked-{case}")
                summary = harness.LocalCollectionHarness(
                    bundle(),
                    solver,
                    runtime,
                    log,
                    teacher_model="synthetic-solver-not-a-teacher",
                ).run_attempt()
                self.assertEqual(summary["status"], "BLOCKED_BACKEND")
                self.assertEqual(solver.invocations, [])
                self.assertEqual(runtime.tool_calls, [])
                self.assertEqual(runtime.cleanup_calls, 1)
                finished = [
                    row for row in log.read() if row["event_type"] == "attempt_finished"
                ]
                self.assertEqual(finished[-1]["status"], "BLOCKED_BACKEND")

    def test_solver_failure_still_cleans_up_and_is_not_review_ready(self):
        solver = FakeSolver([RuntimeError("synthetic provider failure")])
        runtime = FakeRuntime()
        log = self.make_log("solver-failure")
        summary = harness.LocalCollectionHarness(
            bundle(),
            solver,
            runtime,
            log,
            teacher_model="synthetic-solver-not-a-teacher",
        ).run_attempt()
        self.assertEqual(summary["status"], "ATTEMPT_FAILED")
        self.assertEqual(runtime.cleanup_calls, 1)
        self.assertFalse(
            harness.review_acceptance_ready(
                accepted_review(), summary.get("outcomes", []), 2
            )
        )

    def test_verifier_error_records_its_index_and_cannot_pass(self):
        solver = FakeSolver([assistant_final()])
        runtime = FakeRuntime(fail_sql="duplicate_count")
        log = self.make_log("verifier-failure")
        summary = harness.LocalCollectionHarness(
            bundle(),
            solver,
            runtime,
            log,
            teacher_model="synthetic-solver-not-a-teacher",
        ).run_attempt()
        outcomes = [
            row for row in log.read() if row["event_type"] == "verifier_outcome"
        ]
        self.assertEqual([row["verifier_index"] for row in outcomes], [0, 1])
        self.assertTrue(outcomes[0]["passed"])
        self.assertFalse(outcomes[1]["passed"])
        self.assertIn("synthetic verifier transport failure", outcomes[1]["error"])
        self.assertNotEqual(summary["status"], "ACCEPTED")
        self.assertEqual(runtime.cleanup_calls, 1)

    def test_unknown_provider_usage_remains_unknown_not_zero(self):
        solver = FakeSolver([assistant_final()])
        runtime = FakeRuntime()
        log = self.make_log("unknown-usage")
        summary = harness.LocalCollectionHarness(
            bundle(),
            solver,
            runtime,
            log,
            teacher_model="synthetic-solver-not-a-teacher",
        ).run_attempt()
        assistant_events = [
            row for row in log.read() if row["event_type"] == "assistant_message"
        ]
        self.assertEqual(len(assistant_events), 1)
        self.assertIsNone(assistant_events[0].get("usage"))
        self.assertIsNone(summary.get("usage"))

    def test_cleanup_failure_is_recorded_and_never_accepted(self):
        solver = FakeSolver([assistant_final()])
        runtime = FakeRuntime(fail_cleanup=True)
        log = self.make_log("cleanup-failure")
        summary = harness.LocalCollectionHarness(
            bundle(),
            solver,
            runtime,
            log,
            teacher_model="synthetic-solver-not-a-teacher",
        ).run_attempt()
        self.assertEqual(runtime.cleanup_calls, 1)
        cleanup = [row for row in log.read() if row["event_type"] == "cleanup"][-1]
        self.assertFalse(cleanup["success"])
        self.assertIn("synthetic cleanup failure", cleanup["error"])
        self.assertNotEqual(summary["status"], "ACCEPTED")


if __name__ == "__main__":
    unittest.main()
