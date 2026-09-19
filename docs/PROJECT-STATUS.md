# KIANGANA 2.0 — Project Status

Status date: **2026-09-19**

## Current repository state

| Dimension | Classification | Evidence / interpretation |
|---|---|---|
| Repository visibility | **PUBLIC** | GitHub repository metadata |
| Global product version | **UNKNOWN / not formally released** | No product release or tag exists |
| Operating/governance model | **DOCUMENTED** | README, governance, templates, schemas |
| Current Gate Zero validator | **IMPLEMENTED** | `scripts/validate_gate_zero.py` |
| Current main Gate Zero | **TESTED / PASS** | Actions run `35324662670` at `d3790d349e45d794bbb78d46fc1c48862c678151` |
| Current main unit tests | **TESTED / 5 PASS** | Same Actions run |
| KIF presence on current main | **ABSENT** | Current main tree contains no `kif/` directory |
| KIF V0.2 CP-01 | **REPRODUCIBLE checkpoint** | Verified historical branch/commit and dedicated CI |
| Public user-facing demo | **UNKNOWN / not available** | GitHub Pages disabled; no verified public demo found |
| License | **NONE GRANTED** | No root `LICENSE` file; repository metadata license is null |
| GitHub Releases | **NONE** | Releases list empty |
| Git tags | **NONE** | Git tag refs empty |

## Current main CI

Current main is green:

```text
RUN       35324662670
WORKFLOW  Gate Zero
BRANCH    main
HEAD      d3790d349e45d794bbb78d46fc1c48862c678151
RESULT    SUCCESS
```

Observed in logs:

- `GATE ZERO: PASSED`
- 29 required governance artifacts validated
- levels P0–P5 present
- 5 tests run
- 5 tests passed

This workflow validates the **current main governance/evidence surface**. It does **not** execute KIF.

## KIF verified historical checkpoint

```text
CHECKPOINT     KIF V0.2 CP-01 — Dual Provider + Controlled Fallback
LOCATION       branch kif-v0.2-cp01 / verified Git history
PROOF COMMIT   69d3c9a1fdfc9616700572011a466b549be0c867
PROOF RUN      35286354669
LIVE JOB       105419457485
FREEZE COMMIT  57c4bfc2664398383a784128a9fa03dc3e41c0e4
FREEZE RUN     35287044624
CLASSIFICATION REPRODUCIBLE
```

Observed proof:

- DeepSeek model discovery/authenticated real call: PASS
- Groq model `openai/gpt-oss-20b`: PASS
- real Groq call: PASS
- controlled DeepSeek-unavailable → Groq fallback: PASS
- 41/41 unit tests: PASS
- 3/3 integration tests: PASS
- `UsageRecord.provider == "groq"`: PASS
- Groq token observation: 78 input / 62 output / 140 total
- tracked-file secret hygiene in the dedicated KIF workflow: CLEAN
- proof → freeze: one commit, zero files changed

Actual monetary cost was **not observed**. The integration contract keeps `actual_cost=None`.

## Historical Gate Zero failure

At the KIF freeze head, the repository-level Gate Zero workflow failed:

```text
RUN     35287044647
HEAD    57c4bfc2664398383a784128a9fa03dc3e41c0e4
RESULT  FAILURE
```

The failure was caused by the root validator detecting a prohibited credential marker in:

- `kif/source/.env.example`
- `.github/workflows/kif-gate-zero.yml`

This failure remains valid historical evidence.

The later current-main success did **not** retroactively repair that freeze-head tree. The current `main` tree simply does not contain the KIF files that triggered that root scan, and run `35324662670` therefore validates a different, current branch state.

## Status interpretation

Do not generalize module evidence to the whole repository:

- **Current KIANGANA 2.0 main:** PUBLIC / TESTED governance-evidence foundation.
- **KIF V0.2 CP-01:** REPRODUCIBLE historical checkpoint.
- **Whole KIANGANA 2.0 vision:** not fully implemented or production-ready.

## Current limits

Not demonstrated on current `main`:

- KIF source;
- autonomous agents;
- memory/vector database;
- public API;
- UI;
- production deployment;
- public demo;
- real monetary cost accounting.

No new KIF development is implied by this documentation update.
