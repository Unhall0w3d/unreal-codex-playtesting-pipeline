#!/usr/bin/env python3

from __future__ import annotations

import contextlib
import importlib.util
import json
import pathlib
import tempfile
import threading
import unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer


ROOT = pathlib.Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "scripts" / "local-review-openai.py"
SPEC = importlib.util.spec_from_file_location("local_review_openai", MODULE_PATH)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def task() -> dict:
    return {
        "schema_version": 1,
        "task_id": "test.review.001",
        "task_type": "visual_review",
        "required_capabilities": ["input.text", "input.image", "output.closed_json", "review.visual"],
        "objective": "Find obvious visual regressions.",
        "goalposts": [{"id": "materials", "requirement": "No missing material is visible."}],
        "known_non_goals": ["Do not judge final art direction."],
        "images": [{"id": "view-a", "path": "view-a.png"}],
    }


class Handler(BaseHTTPRequestHandler):
    body = None

    def do_POST(self):
        length = int(self.headers["Content-Length"])
        type(self).body = json.loads(self.rfile.read(length))
        candidate = {
            "verdict": "pass",
            "summary": "No missing material is visible in the supplied frame.",
            "findings": [],
            "uncertainties": ["Only one view was supplied."],
            "recommended_followups": ["Capture another fixed angle."],
        }
        response = json.dumps({"choices": [{"message": {"content": json.dumps(candidate)}}]}).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(response)))
        self.end_headers()
        self.wfile.write(response)

    def log_message(self, *_args):
        pass


@contextlib.contextmanager
def server():
    instance = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    thread = threading.Thread(target=instance.serve_forever, daemon=True)
    thread.start()
    try:
        yield instance
    finally:
        instance.shutdown()
        instance.server_close()
        thread.join(timeout=2)


class LocalReviewAdapterTests(unittest.TestCase):
    def test_endpoint_rejects_non_loopback(self):
        with self.assertRaises(MODULE.ContractError):
            MODULE.validate_endpoint("http://192.0.2.1:8080/v1/chat/completions")

    def test_task_rejects_unknown_fields(self):
        with tempfile.TemporaryDirectory() as directory:
            path = pathlib.Path(directory) / "task.json"
            value = task()
            value["shell"] = "do something"
            path.write_text(json.dumps(value))
            with self.assertRaises(MODULE.ContractError):
                MODULE.load_task(path)

    def test_pass_rejects_goalpost_violation_findings(self):
        candidate = {
            "verdict": "pass",
            "summary": "Contradictory result.",
            "findings": [{
                "evidence_id": "policy",
                "goalpost_id": "authority",
                "category": "logic",
                "severity": "major",
                "confidence": 1.0,
                "description": "A violation exists.",
                "evidence": "Explicit evidence.",
            }],
            "uncertainties": [],
            "recommended_followups": [],
        }
        with self.assertRaises(MODULE.ContractError):
            MODULE.validate_candidate(candidate, {"policy": "text/plain"}, {"authority"})

    def test_text_evidence_rejects_bounding_box(self):
        candidate = {
            "verdict": "fail",
            "summary": "One violation.",
            "findings": [{
                "evidence_id": "policy",
                "goalpost_id": "authority",
                "category": "logic",
                "severity": "major",
                "confidence": 1.0,
                "description": "A violation exists.",
                "evidence": "Explicit evidence.",
                "bbox_normalized": [0, 0, 1, 1],
            }],
            "uncertainties": [],
            "recommended_followups": [],
        }
        with self.assertRaises(MODULE.ContractError):
            MODULE.validate_candidate(candidate, {"policy": "text/plain"}, {"authority"})

    def test_image_cannot_escape_evidence_root(self):
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory) / "evidence"
            root.mkdir()
            outside = pathlib.Path(directory) / "outside.png"
            outside.write_bytes(b"\x89PNG\r\n\x1a\n")
            value = task()
            value["images"][0]["path"] = "../outside.png"
            with self.assertRaises(MODULE.ContractError):
                MODULE.load_images(value, root)

    def test_one_bounded_request_returns_provenance_envelope(self):
        with tempfile.TemporaryDirectory() as directory, server() as instance:
            root = pathlib.Path(directory)
            evidence = root / "evidence"
            evidence.mkdir()
            (evidence / "view-a.png").write_bytes(b"\x89PNG\r\n\x1a\nminimal-test-evidence")
            request = root / "task.json"
            request.write_text(json.dumps(task(), separators=(",", ":")))

            args = type("Args", (), {
                "endpoint": f"http://127.0.0.1:{instance.server_port}/v1/chat/completions",
                "request": str(request),
                "evidence_root": str(evidence),
                "model": "test-model",
                "timeout": 5,
                "max_tokens": 256,
            })()
            result = MODULE.run(args)

            self.assertEqual(result["task_id"], "test.review.001")
            self.assertEqual(result["candidate"]["verdict"], "pass")
            self.assertEqual(result["worker"]["model"], "test-model")
            self.assertEqual(len(result["evidence"]), 1)
            self.assertIn("response_format", Handler.body)
            self.assertNotIn(str(evidence), json.dumps(Handler.body))


if __name__ == "__main__":
    unittest.main()
