# JARVIS CORE — BUILD 001

**Status:** IMPLEMENTED (branch proposal; CI evidence pending)  
**Branch:** `feat/jarvis-core-build-001`  
**Base:** `main`

## Objective

Introduce a small, deterministic mission-contract core into KIANGANA 2.0. This is a foundation for future orchestration, not a claim that autonomous agents, memory, a public API, a UI, or production deployment exist.

## Architecture boundary

```text
Human intent
    -> Mission contract
    -> Permission / approval policy
    -> (future bounded executor; NOT IMPLEMENTED HERE)
    -> Tests and evidence
    -> Human acceptance / rejection
```

## Included

- Immutable `Mission` contract with identity, objective, requested actions and state.
- Explicit lifecycle transitions: proposed, approved, running, verified, accepted, rejected, blocked, cancelled.
- Sensitive-action classification for financial transactions, production deployment, irreversible deletion, external communication and billing changes.
- Explicit human approval required before a sensitive mission can enter `approved`.
- Unit tests using only the Python standard library.

## Excluded by design

- No model/provider calls, API keys, secrets or network access.
- No tool execution, GitHub writes from the runtime, transactions, external messages, deletion, billing changes or deployment.
- No persistent memory, vector store, agent loop, scheduler or autonomous approval.
- No claim of actual monetary cost or production readiness.

## #0$ policy

`UNKNOWN` capabilities remain disabled. This build has no paid dependencies and makes no billable API calls. Approval of a mission is a recorded state transition only; it does not execute the requested action. The human remains the final authority.

## Local verification

From the repository root:

```bash
python3 -m unittest discover -s tests -v
python3 scripts/validate_gate_zero.py
```

CI on the pull request is the authoritative execution evidence for this branch. Results must be read from the actual workflow run; this document does not pre-claim a pass.

## Acceptance criteria

1. Existing Gate Zero validator and tests remain unchanged.
2. JARVIS unit tests pass under the repository's Python 3.12 CI.
3. Sensitive actions cannot be approved without the explicit `human_approved=True` input.
4. Invalid lifecycle transitions fail closed.
5. No external side effect occurs in this module.
6. The PR remains unmerged and no deployment is performed pending owner approval.
