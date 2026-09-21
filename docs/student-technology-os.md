# P05-CP-STUDENT-01 — #0$ Student Technology OS Foundation

## Purpose

This checkpoint creates a minimal, testable baseline for KIANGANA 2.0 to discover local engineering capabilities and classify technology resources under the `#0$` doctrine.

It does **not** provision cloud infrastructure, activate billing, call paid APIs, reopen KIF V0.3, or create an agent framework.

## Architecture

```text
HUMAN
  ↓
LOCAL MACHINE
  ↓
CAPABILITY DISCOVERY
  ↓
#0$ CLASSIFICATION
  ↓
MACHINE-READABLE BASELINE
  ↓
AUTOMATED TEST
  ↓
GITHUB CI
  ↓
EVIDENCE
```

## Zero-dollar classes

| Class | Meaning |
|---|---|
| `ZERO_NATIVE` | local/open capability with no direct usage charge |
| `ZERO_STUDENT` | benefit that depends on verified student eligibility |
| `ZERO_QUOTA` | free access constrained by a quota or plan limit |
| `CREDITED` | temporary promotional credit; never a persistent dependency |
| `PAID_OPTIONAL` | paid capability that is disabled by default |

The catalog sets direct spend to `0` and forbids automatic enablement of paid services.

## Files

- `config/capabilities.yaml` — machine-readable capability and economic policy registry.
- `scripts/student_system_baseline.py` — dependency-free local discovery.
- `tests/test_student_system_baseline.py` — policy and discovery tests.
- `.github/workflows/student-foundation.yml` — clean-runner validation and evidence artifact.

The `.yaml` catalog intentionally uses JSON syntax, which is a YAML 1.2 subset. This lets the checkpoint remain Python-standard-library-only.

## What the local probe reads

The script observes only:

- operating system family and release;
- WSL presence markers;
- Python version;
- availability/version output for Git, GitHub CLI, Docker CLI and Codex CLI.

It does not intentionally read or emit credentials, authentication tokens, user names, hostnames, home-directory paths, or cloud account identifiers.

External/student services are deliberately reported as `UNKNOWN_EXTERNAL`. Availability must be proven separately.

## Run locally

From the repository root:

```bash
python3 scripts/student_system_baseline.py
```

Machine-readable output:

```bash
python3 scripts/student_system_baseline.py --json
```

Run the checkpoint tests:

```bash
python3 -m unittest discover -s tests -p 'test_student_system_baseline.py' -v
```

Run the existing repository gate as a regression check:

```bash
python3 scripts/validate_gate_zero.py
python3 -m unittest discover -s tests -v
```

## Interpretation

A local capability can be:

- `PASS` — executable evidence was observed;
- `NOT_AVAILABLE` — the local tool was not found;
- `UNKNOWN_EXTERNAL` — intentionally not probed by this checkpoint.

`LOCAL_FOUNDATION_READY` requires OS, WSL, Git, GitHub CLI, Docker CLI and Python.

Codex CLI is observed but is not required for the core local-ready verdict.

## CI evidence

GitHub Actions runs the baseline on a clean Ubuntu runner, validates the machine-readable result, executes the new tests, and reruns the existing Gate Zero regression suite.

A GitHub-hosted runner is **not evidence of the owner's local WSL state**. Local L2 evidence requires the owner to run the same script on the actual machine and preserve the observed result without secrets.

## Security boundaries

This checkpoint performs no provider API calls itself and does not create cloud resources, enable billing, purchase credits, read provider credentials, persist authentication material, change KIF providers, or execute financial operations.

## Evidence maturity

After CI passes, the implementation may be classified **IMPLEMENTED / CI-TESTED**.

Do not claim the owner's local baseline is `TESTED` until the script has actually been executed on that machine.

Do not claim `REPRODUCIBLE` until a clean reproduction is observed and recorded.
