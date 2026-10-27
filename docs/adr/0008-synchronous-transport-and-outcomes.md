# ADR-0008: Synchronous transport with distinct execution outcomes

- **Status:** Accepted
- **Date:** 2026-10-26
- **Scope:** Knowledge-Based Validation Service (thesis implementation)

## Context

V0 serves one on-demand request at a time (ADR-0002, ADR-0007), and the collaborating subsystem expects validation information for presentation. Asynchronous job handling would add job state, polling/callback semantics, and idempotency concerns before there is evidence that they are needed.

Separately, incomplete *input* and incomplete *execution* were being grouped under one notion of "partial result". They mean different things: missing evidence legitimately yields an unresolved assessment; a timeout does not license a cut-off semantic verdict.

## Decision

V0 uses **synchronous request/response**: one analysis request in, one structured analysis result out, within the same interaction. No async jobs, polling, callbacks, or job-state management in V0.

Three outcome classes are distinguished:

1. **Input Failure** — the request is structurally unusable (ADR-0006, level 1). Explicit; nothing analyzed.
2. **Completed Analysis** — the analysis finished. The result may contain unresolved/partial/insufficient-evidence conclusions caused by artifact/evidence deficiencies. These are legitimate semantic outputs.
3. **Execution Failure** — the request was valid but the analysis did not complete (timeout, cancellation, resource exhaustion, other cutoff). The service must not return an apparently valid semantic partial result; it returns an explicit execution/operational failure.

No error codes, HTTP status codes, or concrete timeout values are defined here. The execution limit remains operational configuration.

Asynchronous transport may later be introduced as a separate adapter around the same analysis core if performance evidence justifies it.

## Consequences

- The subsystem gets one response per request in V0, simplifying its integration.
- Execution failures are visible as failures, not as weak validation claims.
- Artifact-driven unresolved conclusions must be clearly distinguishable from execution cutoffs in the result.
- Long-running analyses block the request; the configured limit must be revisited once workload and graph size are known.
- Any future async adapter must not duplicate the analysis core.

## Alternatives considered

- **Asynchronous jobs now** — more robust for long analyses, but unnecessary complexity before performance evidence.
- **Return partial semantic results on timeout** — risks presenting cut-off analysis as a validation conclusion; rejected.
- **Treat execution failure as an artifact deficiency** — wrong semantics; a timeout says nothing about artifacts.
- **Leave transport unspecified** — acceptable at design level, but obscures the V0 contract.

## Open questions (not decided by this ADR)

- Concrete time bound and how it is configured.
- Cancellation behaviour and cleanup.
- Result envelope details for execution failures.
- Whether the service exposes analysis progress.
- When and how an async adapter would be introduced.
