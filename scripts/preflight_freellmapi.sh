#!/usr/bin/env bash
set -uo pipefail

MODE="${1:---pre}"
ERRORS=0
WARNINGS=0

ok()   { printf '[PASS] %s\n' "$1"; }
warn() { printf '[WARN] %s\n' "$1"; WARNINGS=$((WARNINGS + 1)); }
fail() { printf '[FAIL] %s\n' "$1"; ERRORS=$((ERRORS + 1)); }

need_cmd() {
  if command -v "$1" >/dev/null 2>&1; then
    ok "$1 available: $(command -v "$1")"
  else
    fail "$1 is missing"
  fi
}

printf 'KIANGANA 2.0 — P05-CP03 FreeLLMAPI preflight\n'
printf 'mode=%s\n\n' "$MODE"

case "$MODE" in
  --pre|--post) ;;
  *)
    printf 'Usage: %s [--pre|--post]\n' "$0" >&2
    exit 2
    ;;
esac

if grep -qiE 'microsoft|wsl' /proc/version 2>/dev/null; then
  ok "WSL environment detected"
else
  warn "WSL marker not detected; this is acceptable on native Linux"
fi

need_cmd docker
need_cmd curl
need_cmd openssl

if command -v docker >/dev/null 2>&1; then
  if docker compose version >/dev/null 2>&1; then
    ok "Docker Compose plugin available"
  else
    fail "Docker Compose plugin unavailable"
  fi

  if docker info >/dev/null 2>&1; then
    ok "Docker daemon reachable"
  else
    fail "Docker CLI exists but daemon is not reachable"
  fi
fi

if [ "$MODE" = "--pre" ]; then
  if curl -fsS --max-time 2 http://127.0.0.1:3001/api/ping >/dev/null 2>&1; then
    warn "Port 3001 already serves a FreeLLMAPI-compatible ping endpoint"
  else
    ok "No FreeLLMAPI ping detected on localhost:3001 before installation"
  fi
else
  PING_FILE="$(mktemp)"
  if curl -fsS --max-time 5 http://127.0.0.1:3001/api/ping >"$PING_FILE"; then
    if grep -q '"status"[[:space:]]*:[[:space:]]*"ok"' "$PING_FILE"; then
      ok "FreeLLMAPI /api/ping returned status=ok"
    else
      fail "FreeLLMAPI /api/ping responded but status was not ok"
    fi
  else
    fail "FreeLLMAPI /api/ping is unreachable"
  fi
  rm -f "$PING_FILE"

  if curl -fsS --max-time 5 http://127.0.0.1:3001/v1/openapi.json >/dev/null; then
    ok "OpenAPI document is reachable"
  else
    fail "OpenAPI document is unreachable"
  fi

  if [ -n "${FREELLMAPI_API_KEY:-}" ]; then
    if curl -fsS --max-time 8 \
      -H "Authorization: Bearer ${FREELLMAPI_API_KEY}" \
      http://127.0.0.1:3001/v1/models >/dev/null; then
      ok "Authenticated /v1/models request succeeded"
    else
      fail "Authenticated /v1/models request failed"
    fi
  else
    warn "FREELLMAPI_API_KEY is not set; authenticated model check skipped"
  fi
fi

printf '\nsummary: errors=%s warnings=%s\n' "$ERRORS" "$WARNINGS"
if [ "$ERRORS" -ne 0 ]; then
  exit 1
fi
