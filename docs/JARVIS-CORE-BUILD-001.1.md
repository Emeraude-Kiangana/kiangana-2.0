# JARVIS CORE — BUILD 001.1: APPROVAL HARDENING

**Status:** IMPLEMENTED ON FEATURE BRANCH; CI EVIDENCE PENDING  
**Branch:** `fix/jarvis-core-001-1-approval-hardening`  
**Base:** `main`

## Objective

Close the constructor-level lifecycle bypass identified in the post-merge audit of BUILD 001.

## Changes

- Lifecycle fields (`status`, `human_approved`) are no longer constructor inputs.
- Mission lifecycle state is immutable and can only be advanced through `transition()`.
- Requested actions are normalized to an immutable tuple and validated.
- Every non-empty requested action requires explicit human approval. This deliberately treats unknown/new action names as approval-required rather than implicitly safe.
- Invalid mission inputs, target types and lifecycle transitions fail closed.
- Tests cover constructor injection, mutation, unknown actions, malformed input, approval bypass and skipped lifecycle stages.

## Security boundary

This is an in-process contract, not an authorization service. It does not authenticate the human approver, persist an approval record, bind approval to an identity or cryptographically protect mission state. A caller able to execute arbitrary Python in the same process may still construct or replace objects. Do not treat this module as a production security boundary.

No executor, provider/API calls, secrets, network access, persistence, agent loop, transactions, external communication, deletion, billing changes or deployment are added.

## Verification

Run from repository root:

```bash
python3 -m unittest discover -s tests -v
python3 scripts/validate_gate_zero.py
```

CI is the authoritative test evidence. Do not claim PASS until the actual workflow result is inspected.

## Acceptance criteria

1. BUILD 001 files remain intact except the intended contract hardening and expanded JARVIS tests.
2. Lifecycle state cannot be supplied through the public dataclass constructor.
3. Every mission with requested actions requires explicit approval before entering `approved`.
4. Unknown action names fail closed.
5. Invalid inputs and lifecycle transitions are rejected.
6. No external side effects or paid dependencies are introduced.
7. PR remains unmerged; no deployment is performed without explicit owner approval.
