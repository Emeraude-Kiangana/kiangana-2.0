# P05-CP03 — FreeLLMAPI Adoption Runbook

**Mode:** TOOL-FIRST · #0$ · EVIDENCE-FIRST · FAIL-CLOSED  
**Target:** WSL2 Ubuntu + Docker Desktop  
**Upstream pin:** FreeLLMAPI v0.12.0  
**Rule:** never paste provider credentials into Git, this repository, screenshots, issue comments or evidence records.

## 0. Success definition

P05-CP03 is not complete because a dashboard opens. It is complete only when all gates below are evidenced:

1. WSL2 can reach the Docker daemon.
2. FreeLLMAPI runs locally and returns `status=ok`.
3. The router stays bound to loopback by default.
4. At least two upstream providers are manually approved under the #0$ policy.
5. Authenticated model discovery works.
6. One minimal live request succeeds.
7. Controlled fallback is observed.
8. Local evidence contains no credentials.
9. Stop/start rollback is verified.
10. KIF integration remains a later checkpoint; this mission must not claim it prematurely.

---

## 1. Obtain the KIANGANA checkpoint branch

### If the repository is not cloned

```bash
cd ~
gh repo clone Emeraude-Kiangana/kiangana-2.0
cd kiangana-2.0
git fetch origin
git switch p05-cp03-universal-inference-fabric
```

### If it already exists

Do not overwrite local work.

```bash
cd ~/kiangana-2.0
git status --short
```

Expected safe state: no unexpected output.

Then:

```bash
git fetch origin
git switch p05-cp03-universal-inference-fabric
git pull --ff-only
```

Confirm:

```bash
git branch --show-current
git log -1 --oneline
```

---

## 2. WSL2 / Docker gate

Official Docker WSL documentation:

https://docs.docker.com/desktop/features/wsl/

Check WSL:

```bash
wsl.exe -l -v
```

Ubuntu must show VERSION `2`.

Start Docker Desktop from WSL if needed:

```bash
powershell.exe -NoProfile -Command "Start-Process 'C:\Program Files\Docker\Docker\Docker Desktop.exe'"
```

Then:

```bash
docker version
docker compose version
docker info
```

### If Docker CLI exists but the daemon is unavailable

Open Docker Desktop:

```text
Settings
→ General
→ Use WSL 2 based engine
```

Then:

```text
Settings
→ Resources
→ WSL Integration
→ Ubuntu = ON
→ Apply & Restart
```

Return to WSL and rerun:

```bash
docker info
```

Do not continue until this passes.

---

## 3. KIANGANA preflight

From the KIANGANA repository:

```bash
cd ~/kiangana-2.0
bash scripts/preflight_freellmapi.sh --pre
```

Expected critical lines:

```text
[PASS] docker available
[PASS] Docker Compose plugin available
[PASS] Docker daemon reachable
[PASS] curl available
[PASS] openssl available
```

Warnings are informational. Any `[FAIL]` blocks the checkpoint.

---

## 4. Install a pinned FreeLLMAPI source checkout

Official upstream:

https://github.com/tashfeenahmed/freellmapi

Official install documentation:

https://github.com/tashfeenahmed/freellmapi/blob/main/docs/en/install/01-install.md

Use a separate infrastructure directory. Do not vendor the upstream source into KIANGANA.

```bash
mkdir -p ~/opt
cd ~/opt

git clone https://github.com/tashfeenahmed/freellmapi.git
cd freellmapi

git fetch --tags
git checkout v0.12.0
```

Verify the pinned release target:

```bash
git rev-parse HEAD
```

Expected commit for v0.12.0:

```text
e4a47f203dba3b610dc180f628d3e821abbaf564
```

If the commit differs, stop and investigate before execution.

---

## 5. Generate local encryption material

FreeLLMAPI needs an encryption key for locally stored provider credentials.

Remain in:

```bash
cd ~/opt/freellmapi
```

Then:

```bash
umask 077
ENCRYPTION_KEY="$(openssl rand -hex 32)"
printf 'ENCRYPTION_KEY=%s\nPORT=3001\n' "$ENCRYPTION_KEY" > .env
unset ENCRYPTION_KEY
chmod 600 .env
```

Verify permissions without printing the secret:

```bash
stat -c '%a %n' .env
```

Expected:

```text
600 .env
```

Never run `cat .env` in a recorded terminal or paste its contents into chat.

The upstream Compose file binds port 3001 to `127.0.0.1` by default. Do not set `HOST_BIND=0.0.0.0` during this checkpoint.

---

## 6. Build and boot

Build from the pinned source checkout:

```bash
cd ~/opt/freellmapi
docker compose up -d --build
```

Inspect status:

```bash
docker compose ps
```

Inspect only recent logs:

```bash
docker compose logs --tail=80 freellmapi
```

Health test:

```bash
curl -fsS http://127.0.0.1:3001/api/ping
```

Expected structure:

```json
{"status":"ok","timestamp":"..."}
```

Verify API documentation:

```bash
curl -fsS -o /dev/null -w '%{http_code}\n' \
  http://127.0.0.1:3001/v1/openapi.json
```

Expected:

```text
200
```

---

## 7. Open the local dashboard

From WSL:

```bash
explorer.exe "http://localhost:3001"
```

The browser interaction is intentionally manual because credentials and account setup must stay outside Git automation.

Complete any first-run local admin setup requested by the application.

---

## 8. Add provider 1 — Groq

Official Groq quickstart:

https://console.groq.com/docs/quickstart

Official current rate-limit table:

https://console.groq.com/docs/rate-limits

Create/manage the key from Groq Console. Before adding it, verify the account/project is on the intended free plan and verify the current limits.

In FreeLLMAPI:

```text
Dashboard
→ Keys
→ Groq
→ Add key
→ Test
```

Paste the key only into the FreeLLMAPI local dashboard.

Do not paste it into WSL command history.

---

## 9. Add provider 2 — Google Gemini

Official API-key documentation:

https://ai.google.dev/gemini-api/docs/api-key

Official pricing:

https://ai.google.dev/gemini-api/docs/pricing

Official billing explanation:

https://ai.google.dev/gemini-api/docs/billing

Use a project that is confirmed to remain on the Free Tier for this checkpoint. Do not enable billing merely to satisfy this mission.

In FreeLLMAPI:

```text
Dashboard
→ Keys
→ Google / Gemini
→ Add key
→ Test
```

Again, paste the credential only into the local dashboard.

---

## 10. Build the approved fallback chain

The #0$ policy is authoritative. FreeLLMAPI's catalog is discovery metadata, not independent proof that a route costs zero.

In the dashboard:

1. open the fallback/routing page;
2. enable only models/providers whose current cost class was verified;
3. place the preferred free route first;
4. place the second approved route after it;
5. disable routes whose cost status is unknown;
6. do not activate premium catalog functionality for this checkpoint.

Record model names only. Never record provider keys.

---

## 11. Export the unified local key safely for one shell

FreeLLMAPI generates a unified bearer key for local clients.

In WSL, avoid placing it directly into command history:

```bash
read -rsp "Paste FreeLLMAPI unified key: " FREELLMAPI_API_KEY
echo
export FREELLMAPI_API_KEY
```

The value is now present only in the current shell environment.

Check that the variable exists without printing it:

```bash
test -n "$FREELLMAPI_API_KEY" && echo "FREELLMAPI_API_KEY loaded"
```

---

## 12. Authenticated post-install verification

```bash
cd ~/kiangana-2.0
bash scripts/preflight_freellmapi.sh --post
```

Then run the Python verifier without live inference:

```bash
python3 scripts/verify_freellmapi.py
```

This checks:

- public ping;
- OpenAPI document;
- authenticated model listing;
- evidence-file generation.

The output is written under:

```text
artifacts/private/P05-CP03-local-verification.json
```

That directory is ignored by Git.

---

## 13. Human-gated live inference

The verifier refuses live inference unless the operator explicitly unlocks it.

First confirm the fallback chain contains only approved routes.

Then:

```bash
export KIANGANA_ALLOW_LIVE_INFERENCE=YES
python3 scripts/verify_freellmapi.py --live
unset KIANGANA_ALLOW_LIVE_INFERENCE
```

A successful run must report the served model and latency without printing the credential.

Immediately remove the unified key from the shell after the test if it is no longer needed:

```bash
unset FREELLMAPI_API_KEY
```

---

## 14. Deterministic fallback proof

This proof uses the synthetic provider in:

```text
scripts/failover_probe_server.py
```

It contains no real model and no real credential.

### Terminal A — start the probe healthy

For Docker Desktop, first try loopback:

```bash
cd ~/kiangana-2.0
python3 scripts/failover_probe_server.py
```

In Terminal B:

```bash
curl -fsS http://127.0.0.1:18080/control/status
curl -fsS http://127.0.0.1:18080/v1/models
```

If the FreeLLMAPI container cannot reach the WSL loopback service, stop Terminal A with `Ctrl+C` and restart the probe bound to the WSL interface:

```bash
export KIANGANA_PROBE_HOST=0.0.0.0
python3 scripts/failover_probe_server.py
```

Get the WSL address:

```bash
hostname -I | awk '{print $1}'
```

Use that address only for the temporary synthetic probe and stop it immediately after the test.

### Register the synthetic provider

In the FreeLLMAPI local dashboard, add a custom OpenAI-compatible provider.

Preferred base URL when reachable from the container:

```text
http://host.docker.internal:18080/v1
```

If that route cannot reach the WSL process, use:

```text
http://<WSL_IP>:18080/v1
```

Synthetic model ID:

```text
kiangana-failover-probe
```

The probe ignores authorization. If the UI requires a non-empty local test credential, use a clearly non-secret synthetic value such as `kiangana-probe-local`.

While the probe is healthy, test the route.

Place this synthetic model first in a temporary fallback profile and one approved real free-tier model second.

### Trigger deterministic failure

Immediately before sending the request:

```bash
curl -fsS -X POST http://127.0.0.1:18080/control/fail
curl -fsS http://127.0.0.1:18080/control/status
```

Expected status:

```json
{"mode":"fail"}
```

Now send one request through the temporary profile from FreeLLMAPI. The synthetic primary returns HTTP 429. The expected successful result must be served by the second approved provider.

Capture only:

- time;
- synthetic primary model name;
- observed 429;
- real fallback model name;
- latency;
- token usage if returned.

Never capture keys.

Restore the probe:

```bash
curl -fsS -X POST http://127.0.0.1:18080/control/healthy
```

Then remove or disable the synthetic provider/profile and stop Terminal A with `Ctrl+C`.

---

## 15. Rollback proof

Stopping the inference fabric must be simple and reversible.

```bash
cd ~/opt/freellmapi
docker compose stop
```

Verify the endpoint is no longer available:

```bash
if curl -fsS --max-time 2 http://127.0.0.1:3001/api/ping >/dev/null; then
  echo "FAIL: endpoint still reachable"
else
  echo "PASS: endpoint stopped"
fi
```

Restart:

```bash
docker compose start
curl -fsS http://127.0.0.1:3001/api/ping
```

Do not run `docker compose down -v` during normal rollback because `-v` removes the persistent volume.

---

## 16. Final local audit

Return to KIANGANA:

```bash
cd ~/kiangana-2.0

git status --short
python3 scripts/validate_gate_zero.py
python3 -m unittest discover -s tests -v
bash -n scripts/preflight_freellmapi.sh
python3 -m py_compile scripts/verify_freellmapi.py scripts/failover_probe_server.py
```

There should be no generated secret files staged for commit.

Inspect ignored evidence explicitly:

```bash
git check-ignore -v artifacts/private/P05-CP03-local-verification.json
```

Expected: the file is ignored by `.gitignore`.

---

## 17. Checkpoint close criteria

Only after the manual evidence exists should `evidence/EVD-2026-005.yaml` be updated from:

```text
PENDING_MANUAL_EXECUTION
```

to a verified state.

Do not claim KIF integration at P05-CP03. The next checkpoint is responsible for the actual KIF adapter:

```text
P05-CP04 — KIF Universal Inference Adapter
TaskEnvelope
  -> KIANGANA policy
  -> FreeLLMAPI-compatible adapter
  -> ResponseEnvelope
  -> UsageRecord
```

That checkpoint must preserve the historical direct-provider fallback path as a recovery route until the new fabric is independently reproduced.
