# ADR-0005 — FreeLLMAPI as Universal Inference Fabric candidate

- **Status:** Accepted for controlled adoption checkpoint
- **Date:** 2026-09-28
- **Project:** KIANGANA 2.0 / P05
- **Checkpoint:** P05-CP03
- **Decision authority:** Emeraude Kiangana

## Context

The verified historical KIF V0.2 CP-01 proves direct DeepSeek/Groq adapters and deterministic fallback, but that source is not present on current `main`. Rebuilding provider-specific routing for every new LLM provider would increase code, operational burden and regression surface.

FreeLLMAPI is evaluated as an external, self-hosted, OpenAI-compatible inference broker. It can normalize multiple upstream providers behind a local endpoint while retaining the option to keep direct KIF adapters as an escape hatch.

## Decision

Adopt FreeLLMAPI only as a **candidate inference fabric below KIF**, never as the policy authority for KIANGANA 2.0.

The intended dependency direction is:

```text
Human intent
  -> KIANGANA policy / #0$ cost guard
  -> KIF execution layer
  -> Universal Inference Fabric
  -> FreeLLMAPI
  -> approved upstream provider
```

FreeLLMAPI does **not** replace:

- human final authority;
- the #0$ cost guard;
- KIANGANA evidence requirements;
- KIF task and result contracts;
- direct-provider adapters retained for recovery or controlled exceptions.

## Guardrails

1. Default deployment is local-only.
2. No provider is treated as zero-cost merely because FreeLLMAPI can route to it.
3. Only explicitly approved free/free-tier routes may enter the default KIANGANA chain.
4. Unknown cost means blocked.
5. Provider credentials are entered locally and never committed.
6. Live inference requires an explicit operator action.
7. Production or multi-user exposure is out of scope.
8. A rollback path must exist: stop FreeLLMAPI and restore direct KIF routing.

## Consequences

### Positive

- one normalized inference endpoint;
- provider failover moves below KIF;
- lower coupling between KIF and provider SDKs;
- easier experimentation with capability-based routing;
- clearer separation between policy, execution and inference transport.

### Negative / unresolved

- upstream free tiers remain unstable;
- provider terms remain independently binding;
- catalog metadata is not proof of actual monetary cost;
- FreeLLMAPI becomes an additional local dependency;
- current KIANGANA `main` still lacks the KIF runtime source, so integration is not yet proven.

## Exit criteria

This ADR moves from architectural decision to reproduced capability only after P05-CP03 records:

- local Docker boot;
- `/api/ping` success;
- authenticated model listing;
- at least two approved zero-cost/free-tier upstream providers;
- observed controlled failover;
- captured non-secret evidence;
- explicit rollback verification;
- KIF adapter integration in a later checkpoint.
