# KIANGANA 2.0 Documentation

## Source-of-truth map

KIANGANA 2.0 separates the current repository state from verified historical checkpoints.

- [Root README](../README.md) — product overview, current capabilities, quick start, KIF relationship and evidence.
- [Project Status](PROJECT-STATUS.md) — factual current status, current CI and historical KIF checkpoint.
- [Architecture](architecture.md) — current-main architecture versus historical KIF execution architecture.
- [GitHub Documentation Standard v1.0](GITHUB-DOCUMENTATION-STANDARD-v1.0.md) — evidence-first documentation rules.
- [Governance](../GOVERNANCE.md) — human authority and internal operating boundaries.
- [Security](../SECURITY.md) — secret handling and prohibited-by-default actions.

## Current main

The current `main` branch is a tested governance/evidence foundation. Its root Gate Zero workflow validates repository artifacts, permission levels and five unit tests.

Current main Gate Zero evidence:

- commit `d3790d349e45d794bbb78d46fc1c48862c678151`
- Actions run `35324662670`
- result: **SUCCESS**

KIF is **not present in the current main tree**.

## KIF checkpoint

KIF — Kiangana Intelligence Fabric — is a module of KIANGANA 2.0 with a verified historical V0.2 CP-01 checkpoint.

Evidence anchors:

- proof commit `69d3c9a1fdfc9616700572011a466b549be0c867`
- live proof run `35286354669`
- live job `105419457485`
- freeze commit `57c4bfc2664398383a784128a9fa03dc3e41c0e4`
- freeze run `35287044624`
- historical branch `kif-v0.2-cp01`

The checkpoint demonstrated real DeepSeek and Groq interactions, deterministic fallback, normalized responses, usage persistence and dedicated CI.

## Historical material

These directories remain inspectable historical/governance records:

- `governance/`
- `missions/`
- `reports/`
- `evidence/`
- `research/`
- `dashboard/`

References to eCDF, AGRICHAIN DAO and the Open Technologies Portfolio describe earlier orchestration/research work. They do not mean those projects are current KIANGANA 2.0 sub-products.

## Documentation rule

Use the repository vocabulary conservatively:

`DOCUMENTED → IMPLEMENTED → TESTED → REPRODUCIBLE`

Do not promote the whole repository because one module has stronger evidence.

Public repository visibility is not a production-readiness claim and is not an open-source license.
