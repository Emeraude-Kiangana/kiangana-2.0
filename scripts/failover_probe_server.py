#!/usr/bin/env python3
"""Controllable synthetic provider for deterministic FreeLLMAPI failover proof.

The server contains no model and no credential. It can answer a valid synthetic
OpenAI-compatible completion while healthy, then be switched to HTTP 429 mode.
This makes the failure condition deliberate and reproducible.

Control endpoints:
  GET  /control/status
  POST /control/healthy
  POST /control/fail
"""

from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import os
import time

HOST = os.environ.get("KIANGANA_PROBE_HOST", "127.0.0.1")
PORT = int(os.environ.get("KIANGANA_PROBE_PORT", "18080"))
MODEL_ID = "kiangana-failover-probe"
FAIL_MODE = False


class Handler(BaseHTTPRequestHandler):
    server_version = "KIANGANA-Failover-Probe/0.2"

    def log_message(self, fmt, *args):
        print("[probe] " + (fmt % args))

    def _json(self, status, payload, extra_headers=None):
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        if extra_headers:
            for key, value in extra_headers.items():
                self.send_header(key, value)
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        global FAIL_MODE
        if self.path.rstrip("/") == "/v1/models":
            self._json(200, {
                "object": "list",
                "data": [{
                    "id": MODEL_ID,
                    "object": "model",
                    "owned_by": "kiangana-local-probe",
                }],
            })
            return
        if self.path.rstrip("/") == "/control/status":
            self._json(200, {"mode": "fail" if FAIL_MODE else "healthy"})
            return
        self._json(404, {"error": {"message": "not found", "type": "not_found"}})

    def do_POST(self):
        global FAIL_MODE
        path = self.path.rstrip("/")

        if path == "/control/healthy":
            FAIL_MODE = False
            self._json(200, {"mode": "healthy"})
            return

        if path == "/control/fail":
            FAIL_MODE = True
            self._json(200, {"mode": "fail"})
            return

        if path == "/v1/chat/completions":
            length = int(self.headers.get("Content-Length", "0") or "0")
            if length:
                self.rfile.read(length)

            if FAIL_MODE:
                self._json(
                    429,
                    {
                        "error": {
                            "message": "intentional KIANGANA fallback probe",
                            "type": "rate_limit_error",
                            "code": "KIANGANA_PROBE_429",
                        }
                    },
                    {"Retry-After": "1"},
                )
                return

            self._json(200, {
                "id": "kiangana-probe-response",
                "object": "chat.completion",
                "created": int(time.time()),
                "model": MODEL_ID,
                "choices": [{
                    "index": 0,
                    "message": {"role": "assistant", "content": "KIANGANA_PROBE_HEALTHY"},
                    "finish_reason": "stop",
                }],
                "usage": {"prompt_tokens": 1, "completion_tokens": 1, "total_tokens": 2},
            })
            return

        self._json(404, {"error": {"message": "not found", "type": "not_found"}})


if __name__ == "__main__":
    print(f"KIANGANA fallback probe listening on http://{HOST}:{PORT}")
    print("Use POST /control/fail immediately before the fallback test.")
    ThreadingHTTPServer((HOST, PORT), Handler).serve_forever()
