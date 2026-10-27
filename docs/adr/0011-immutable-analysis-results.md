# ADR-0011: Immutable analysis results, distinct from external validation links

- **Status:** Accepted
- **Date:** 2026-10-26
- **Scope:** Knowledge-Based Validation Service / external subsystem boundary

## Context

Analysis results support inspection, historical comparison, debugging, and empirical evaluation. If results were overwritten by later analyses, earlier conclusions could not be audited and provenance would collapse.

The subsystem already owns user-facing Scenario–Test links and their lifecycle. The thesis service's analytical history is a different artifact with a different owner.

Execution can also fail after a valid request (ADR-0008). Persisting a cut-off result as if it were a completed one would misrepresent analysis quality.

## Decision

Completed Analysis Results are **first-class persistent research state** of the thesis service.

Each completed Analysis Run has an **immutable, run-addressable** result linked to the exact context that produced it:

```text
artifact identities + revisions -> UKG version -> analysis run -> immutable result
```

A persisted result is traceable to the Analysis Scope; the relevant process, scenario, test case, and evidence identities; their revisions; the UKG version; and the Analysis Run.

Results are never overwritten. A later run over changed artifacts, a new UKG version, or a changed analysis method produces a new result; earlier results remain intact.

**Analysis Result != external Scenario–Test validation link.** The service owns analytical result history. The external subsystem continues to own user-facing link persistence, presentation, and external link lifecycle. Result retention transfers no link ownership.

Completed runs persist results that may include supported, contradicted, unresolved, or insufficient-evidence conclusions and artifact-level diagnostics. Failed runs retain run/failure metadata only; no incomplete semantic result is persisted or presented as valid.

Not decided here: physical storage, retention duration, deletion/archival, compression, persistence of intermediate reasoning artifacts (prompts, raw LLM responses, queries, embeddings, logs), and result caching/reuse mechanics.

## Consequences

- Result history grows monotonically; retention policy becomes necessary later.
- Each result can be compared with others only through explicit run/context identity.
- The subsystem cannot treat a re-analysis as an update to prior conclusions; it receives a new result.
- Failed runs remain visible as failures without polluting the result history.
- Result ownership and link ownership stay cleanly separated between the two systems.

## Alternatives considered

- **Overwrite/update results in place** — simple current-state view, but destroys auditability and comparison.
- **Return results only, store nothing** — offloads history to the subsystem, which owns links, not analytical provenance.
- **Store only summaries** — hides evidence and explanations needed for evaluation and debugging.
- **Persist incomplete results from failed runs** — violates the input-vs-execution distinction and risks invalid conclusions.

## Open questions (not decided by this ADR)

- Physical result storage technology.
- Retention duration and deletion/archival policy.
- Result compression.
- Whether intermediate reasoning artifacts are stored.
- Result caching and reuse mechanics.
- How the subsystem retrieves historical results, if at all.
