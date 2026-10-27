# ADR-0010: Repeatable, non-idempotent analysis runs

- **Status:** Accepted
- **Date:** 2026-10-26
- **Scope:** Knowledge-Based Validation Service / external subsystem contract

## Context

The service is on demand and synchronous (ADR-0002, ADR-0008), and the UKG is versioned per artifact state (ADR-0005). The subsystem may retry after a lost response or issue concurrent requests for the same scope.

Describing the operation as idempotent would be inaccurate: the service has internal persistent state (UKG versions and run identities), even though it does not mutate external artifacts or links. Promising deterministic output would also be premature, since the reasoning mechanism is unselected and could later include probabilistic components.

## Decision

For V0:

- repeated requests for the same scope and artifact revisions: allowed;
- concurrent requests: allowed;
- each accepted request produces its own Analysis Run;
- a compatible persisted UKG version may be reused across runs;
- no duplicate-request suppression;
- no per-scope serialization;
- no ordering guarantee between concurrent runs;
- no locking semantics;
- no exactly-once execution;
- no exact replay of a previous run;
- no promise of deterministic analytical output.

A retry is operationally acceptable but may produce a new run identity. The analysis request itself does not mutate BPMN models, scenarios, test cases, or external Scenario–Test links. Any future exact retry deduplication requires a separate request/idempotency-key contract decision.

The required property is traceability and reproducibility of the **analysis context** (artifact identities/revisions, UKG version, run), not byte-identical output. Not guaranteeing determinism does not mean results must vary; it only declines to promise byte-identical output before the reasoning mechanism is selected.

## Consequences

- The subsystem must tolerate multiple runs for the same artifact state and must not infer "same result" from "same scope".
- Results carry run identity, so comparisons are always between identifiable runs.
- Lost-response retries are safe externally but leave extra internal run records.
- Locks, queues, transactions, scheduling, and idempotency-key mechanics remain undecided and undeveloped.
- Determinism is not a contract property in V0.

## Alternatives considered

- **Strict idempotency by scope/revisions** — simpler retries, but implies deduplication semantics and result equality that V0 cannot promise.
- **Per-scope serialization** — avoids concurrent runs but adds coordination without an established need.
- **Promise deterministic replay** — impossible to guarantee before the reasoning mechanism is selected.
- **Treat runs as disposable/no identity** — would break traceability and result comparison.

## Open questions (not decided by this ADR)

- Whether an idempotency key is needed later.
- Run retention and cleanup.
- How many runs are kept per UKG version.
- Whether concurrent runs may share intermediate computation.
- Which reproducibility metadata (e.g. analysis-method version) results should record.
