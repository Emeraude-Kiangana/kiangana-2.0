#!/usr/bin/env python3
"""Deterministic loopback-only provider used to prove FreeLLMAPI fallback.

GET /v1/models returns one synthetic model.
POST /v1/chat/completions always returns HTTP 429.
No credential is accepted, stored, logged or required.
"""

from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json

HOST = "127.0.0.1"
PORT = 18080
MODEL_ID = "kiangana-failover-probe"


class Handler(BaseHTTPRequestHandler):
    server_version = "KIANGANA-Failover-Probe/0.1"

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
        self._json(404, {"error": {"message": "not found", "type": "not_found"}})

    def do_POST(self):
        if self.path.rstrip("/") == "/v1/chat/completions":
            length = int(self.headers.get("Content-Length", "0") or "0")
            if length:
                self.rfile.read(length)
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
        self._json(404, {"error": {"message": "not found", "type": "not_found"}})


if __name__ == "__main__":
    print(f"KIANGANA fallback probe listening on http://{HOST}:{PORT}/v1")
    print("Expected behavior: every chat request returns HTTP 429.")
    ThreadingHTTPServer((HOST, PORT), Handler).serve_forever()
