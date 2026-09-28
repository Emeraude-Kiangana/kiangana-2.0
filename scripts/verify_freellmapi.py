#!/usr/bin/env python3
"""P05-CP03 local verifier.

No provider credential is persisted or printed. Evidence is written under
artifacts/private/, which is ignored by the repository.
"""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import sys
import time
import urllib.error
import urllib.request

BASE_URL = os.environ.get("FREELLMAPI_BASE_URL", "http://127.0.0.1:3001").rstrip("/")
ROOT = Path(__file__).resolve().parents[1]
EVIDENCE_DIR = ROOT / "artifacts" / "private"


def request_json(path: str, *, method: str = "GET", body: dict | None = None, api_key: str | None = None):
    headers = {"Accept": "application/json"}
    data = None
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
    if body is not None:
        headers["Content-Type"] = "application/json"
        data = json.dumps(body).encode("utf-8")
    req = urllib.request.Request(BASE_URL + path, data=data, headers=headers, method=method)
    started = time.perf_counter()
    with urllib.request.urlopen(req, timeout=30) as response:
        raw = response.read().decode("utf-8")
        elapsed_ms = round((time.perf_counter() - started) * 1000, 2)
        parsed = json.loads(raw)
        interesting_headers = {}
        for key in ("x-routed-via", "x-request-id", "x-model"):
            value = response.headers.get(key)
            if value:
                interesting_headers[key] = value
        return parsed, elapsed_ms, interesting_headers


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--live", action="store_true", help="run one minimal live inference request")
    args = parser.parse_args()

    record = {
        "checkpoint": "P05-CP03",
        "base_url": BASE_URL,
        "checks": [],
        "live_inference": False,
    }

    try:
        ping, latency, _ = request_json("/api/ping")
        assert ping.get("status") == "ok"
        record["checks"].append({"name": "ping", "status": "PASS", "latency_ms": latency})
        print("[PASS] /api/ping")
    except Exception as exc:
        record["checks"].append({"name": "ping", "status": "FAIL", "error_type": type(exc).__name__})
        print(f"[FAIL] /api/ping: {type(exc).__name__}", file=sys.stderr)
        return 1

    try:
        _, latency, _ = request_json("/v1/openapi.json")
        record["checks"].append({"name": "openapi", "status": "PASS", "latency_ms": latency})
        print("[PASS] /v1/openapi.json")
    except Exception as exc:
        record["checks"].append({"name": "openapi", "status": "FAIL", "error_type": type(exc).__name__})
        print(f"[FAIL] /v1/openapi.json: {type(exc).__name__}", file=sys.stderr)
        return 1

    api_key = os.environ.get("FREELLMAPI_API_KEY")
    if not api_key:
        print("[WARN] FREELLMAPI_API_KEY not set; authenticated checks skipped")
        record["checks"].append({"name": "models", "status": "SKIPPED", "reason": "missing local env key"})
    else:
        try:
            models, latency, _ = request_json("/v1/models", api_key=api_key)
            count = len(models.get("data", [])) if isinstance(models, dict) else None
            record["checks"].append({"name": "models", "status": "PASS", "latency_ms": latency, "model_count": count})
            print(f"[PASS] /v1/models models={count}")
        except Exception as exc:
            record["checks"].append({"name": "models", "status": "FAIL", "error_type": type(exc).__name__})
            print(f"[FAIL] /v1/models: {type(exc).__name__}", file=sys.stderr)
            return 1

    if args.live:
        if os.environ.get("KIANGANA_ALLOW_LIVE_INFERENCE") != "YES":
            print("[BLOCK] set KIANGANA_ALLOW_LIVE_INFERENCE=YES for this shell to authorize one live request", file=sys.stderr)
            return 2
        if not api_key:
            print("[BLOCK] FREELLMAPI_API_KEY is required for live inference", file=sys.stderr)
            return 2

        payload = {
            "model": "auto",
            "messages": [{"role": "user", "content": "Reply with exactly KIANGANA_P05_CP03_OK"}],
            "temperature": 0,
            "max_tokens": 32,
        }
        try:
            response, latency, headers = request_json(
                "/v1/chat/completions",
                method="POST",
                body=payload,
                api_key=api_key,
            )
            choice = (response.get("choices") or [{}])[0]
            content = ((choice.get("message") or {}).get("content") or "")[:200]
            usage = response.get("usage")
            record["live_inference"] = True
            record["checks"].append({
                "name": "live_inference",
                "status": "PASS",
                "latency_ms": latency,
                "served_model": response.get("model"),
                "route_headers": headers,
                "usage": usage,
                "output_sample": content,
            })
            print(f"[PASS] live inference model={response.get('model')} latency_ms={latency}")
        except urllib.error.HTTPError as exc:
            record["checks"].append({"name": "live_inference", "status": "FAIL", "http_status": exc.code})
            print(f"[FAIL] live inference HTTP {exc.code}", file=sys.stderr)
            return 1
        except Exception as exc:
            record["checks"].append({"name": "live_inference", "status": "FAIL", "error_type": type(exc).__name__})
            print(f"[FAIL] live inference: {type(exc).__name__}", file=sys.stderr)
            return 1

    EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)
    destination = EVIDENCE_DIR / "P05-CP03-local-verification.json"
    destination.write_text(json.dumps(record, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"[PASS] non-secret local evidence written to {destination.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
