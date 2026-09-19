# KIANGANA 2.0

**KIANGANA 2.0 is an umbrella project for a personal human–AI operating system. The current `main` branch contains a tested governance and evidence foundation; a verified historical KIF checkpoint demonstrates the AI execution layer.**

| Surface | Current verified state |
|---|---|
| Repository | **PUBLIC / TESTED** |
| Global version | **Not formally released** |
| Current main CI | **PASS** — Gate Zero run `35324662670` |
| KIF checkpoint | **V0.2 CP-01 — REPRODUCIBLE** |
| KIF location | Verified Git history / branch `kif-v0.2-cp01`; **not present on current `main`** |
| Demo | **Not publicly available yet** |
| License | **No license currently granted** |
| Maintainer | **Emeraude Kiangana** |

## What it is

KIANGANA 2.0 is the umbrella system. Its current repository surface focuses on controlled project execution, human approval boundaries, evidence capture, mission contracts, validation scripts and CI.

The broader direction is a personal human–AI operating system for structured AI execution, tool orchestration and personal workflows. Those broader capabilities are **vision unless separately backed by code and tests**.

The current product rule is simple:

`human intent → controlled execution → test → evidence → improvement`

## KIF — Kiangana Intelligence Fabric

**KIF is a technical module inside KIANGANA 2.0, not the whole project.**

KIF V0.2 CP-01 exists as a verified historical checkpoint in Git history. It is not part of the current `main` tree.

At the frozen checkpoint, KIF implements:

- a `ModelProvider` abstraction;
- DeepSeek and Groq provider adapters;
- deterministic primary → fallback routing;
- normalized `ResponseEnvelope` output;
- token usage capture in `Usage`;
- append-only JSONL `UsageRecord` persistence;
- a small CLI;
- unit and live integration tests;
- dedicated GitHub Actions workflows.

The proven fallback policy allows Groq only after `TIMEOUT`, `PROVIDER_DOWN`, `RATE_LIMIT` or `QUOTA_EXHAUSTED`. `AUTH_ERROR` and `INVALID_REQUEST` do not trigger fallback.

## What currently works

### Current `main`

The current branch has executed evidence for:

- required Gate Zero repository artifacts;
- governance permission levels P0–P5;
- human final-authority wording;
- mission/evidence schemas and project registry checks;
- secret-marker checks over tracked text files;
- five current Gate Zero unit tests;
- GitHub Actions validation on Python 3.12.

Current `main` Gate Zero: **PASS** — run `35324662670`.

### Verified KIF checkpoint

KIF V0.2 CP-01 has executed evidence for:

- real DeepSeek API interaction;
- real Groq API interaction;
- Groq model match for `openai/gpt-oss-20b`;
- controlled DeepSeek-unavailable → Groq fallback;
- 41/41 unit tests;
- 3/3 integration tests;
- normalized provider responses;
- `task_id` preservation;
- Groq usage persistence;
- observed Groq token values: 78 input, 62 output, 140 total;
- protected Gate Zero files unchanged at the checkpoint;
- tracked-file secret hygiene clean.

**Token usage is demonstrated. Actual monetary cost is not demonstrated.**

## Quick start

### Current KIANGANA 2.0 main

```bash
git clone https://github.com/Emeraude-Kiangana/kiangana-2.0.git
cd kiangana-2.0

python3 scripts/validate_gate_zero.py
python3 -m unittest discover -s tests -v
```

Expected current scope: governance/evidence validation, not KIF execution.

### Reproduce the frozen KIF checkpoint

KIF is not on current `main`. Use the exact freeze commit:

```bash
git clone https://github.com/Emeraude-Kiangana/kiangana-2.0.git
cd kiangana-2.0
git checkout 57c4bfc2664398383a784128a9fa03dc3e41c0e4

cd kif/source
python -m pip install -e ".[dev]"
pytest tests/unit -q
```

For live integration tests, provide your own `DEEPSEEK_API_KEY` and `GROQ_API_KEY` through the environment, then run:

```bash
pytest tests/integration -q -s
```

Do not commit credentials.

## Verified checkpoint

**KIF V0.2 CP-01 — Dual Provider + Controlled Fallback**

- Proof commit: `69d3c9a1fdfc9616700572011a466b549be0c867`
- Proof run: `35286354669`
- Live job: `105419457485`
- Freeze commit: `57c4bfc2664398383a784128a9fa03dc3e41c0e4`
- Freeze run: `35287044624`
- Proof → freeze: **1 commit, 0 files changed**

The freeze commit preserves the exact proof tree.

## Evidence

| Claim | Evidence | Status |
|---|---|---|
| Current main Gate Zero is green | Actions run `35324662670` at `d3790d349...` | **TESTED** |
| Current main tests | 5 tests passed in run `35324662670` | **TESTED** |
| KIF real providers + fallback | Actions run `35286354669`, live job `105419457485` | **REPRODUCIBLE checkpoint** |
| KIF token usage | Same live job: 78 input / 62 output / 140 total | **TESTED** |
| KIF proof tree | commit `69d3c9a1...` | **IMPLEMENTED** |
| KIF frozen tree | commit `57c4bfc...`; zero-file diff from proof | **REPRODUCIBLE checkpoint** |
| Historical root Gate Zero at KIF freeze head | run `35287044647` | **FAILURE — historical** |
| Current documentation baseline | commit `d3790d349...` | **DOCUMENTED** |

The historical Gate Zero failure is not hidden. At the KIF freeze head, the root scanner failed because it found a prohibited credential marker in KIF-tracked files. Current `main` later passed because those KIF files are **not present in the current main tree**. The historical failure is therefore preserved rather than retroactively rewritten.

## Architecture

### Current main

`Human intent → mission contract → bounded execution → tests/evidence → human validation → closure`

### Historical KIF V0.2 checkpoint

```text
TaskEnvelope
    ↓
Router
    ├── DeepSeekAdapter
    │      └── allowed provider failure
    ↓
GroqAdapter
    ↓
ResponseEnvelope
    ↓
UsageRecord
```

See [docs/architecture.md](docs/architecture.md) for the separation between current-main architecture and the historical KIF execution layer.

## Repository structure

Current `main` contains:

```text
governance/   permissions, decisions, project registry
schemas/      mission contract schema
scripts/      Gate Zero validator
tests/        current main Gate Zero tests
evidence/     historical mission evidence records
missions/     mission contracts
reports/      mission reports
docs/         documentation and status
research/     historical research artifacts
```

`kif/` is intentionally **not listed as a current-main directory** because it exists only in the verified historical checkpoint/branch.

## Security

The repository requires human approval boundaries and prohibits committing secrets. Sensitive external actions such as real financial transactions, irreversible deletion, billing changes and production deployment remain prohibited by default unless explicitly authorized.

These are **internal governance controls**, not an external security or AI-safety certification.

See [SECURITY.md](SECURITY.md) and [GOVERNANCE.md](GOVERNANCE.md).

## Limitations

Current limits are explicit:

- KIF is absent from the current `main` tree;
- no public user-facing demo is available;
- no formal KIANGANA 2.0 release or Git tag exists;
- no repository license is currently granted;
- current main does not prove agents, memory, vector databases, autonomous workflows, a public API, a UI or production deployment;
- KIF token usage is observed, but actual monetary cost is `None` in the verified integration;
- current main Gate Zero and historical KIF CI are separate validation surfaces.

## Historical foundation

Gate Zero, mission contracts, P0–P5 permissions, eCDF research and earlier orchestration experiments remain part of the repository history and documentation. They are retained as foundations, but they no longer define the product headline.

References to eCDF, AGRICHAIN DAO and the Open Technologies Portfolio in governance/research files describe historical orchestration work. They should not be interpreted as current sub-products of KIANGANA 2.0.

## Version

- **KIANGANA 2.0 global version:** not formally released.
- **KIF verified module checkpoint:** V0.2 CP-01.
- **KIF package metadata at freeze:** `0.0.1`.

There are currently **no GitHub Releases and no Git tags** for KIANGANA 2.0.

## License

No `LICENSE` file exists at the repository root. Public visibility does not grant an open-source license.

**License decision required from the owner before reuse rights are granted.**

## Author

**Emeraude Kiangana**  
Founder / Builder — Open Technologies

© EMERAUDE KIANGANA — Open Technologies 🇨🇩
