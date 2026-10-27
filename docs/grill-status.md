# Grill Checkpoint — Scope & System Boundary

- **Updated:** 2026-10-26
- **Status:** concluded — Scope & System Boundary (Q1–Q11 answered; no pending question)
- **Purpose:** durable state so a later session can resume without rereading the conversation. Sources of truth remain `README.md`, `CONTEXT.md`, and `docs/adr/`.

## Confirmed decisions

| Decision | Where |
| --- | --- |
| On-demand invocation; subsystem decides when; one request -> one result | ADR-0002 |
| Analysis unit is an Analysis Scope with a process-level default; ownership != participation; declared membership authoritative; no silent expansion; extensible to composite/application scopes | ADR-0007 (amends ADR-0002) |
| Input is self-contained with stable artifact identity (id, type, source system, revision, maybe content hash); no fetch-back for V0 inputs | ADR-0003 |
| UKG persists and is versioned per analysis-scope artifact state; Artifact Version != UKG Version != Analysis Run | ADR-0001, ADR-0005 |
| Three levels: request-level fatal failure, artifact/input diagnostic, research-level conclusion; input inconsistency is not automatically a gap | ADR-0006 |
| Structural coverage/traceability allowed as internal analysis, not a coverage deliverable; three gap situations | ADR-0004 |
| Synchronous transport in V0; Input Failure, Completed Analysis, Execution Failure are distinct; no semantic partial result on cutoff | ADR-0008 |
| Actor model: external subsystem only operational system actor; end user indirect; researcher + harness in evaluation context; no LLM/embedding/solver/vector-DB/test-runner/modeler actors | `README.md` |
| Negative boundary (no test execution/generation, no authoring, no UI/link-store ownership, no ground-truth generation, no autonomous stakeholder substitute) | `README.md` |
| Identifier ownership: subsystem owns scope/artifact ids; service mints UKG version + run id; request id is not a run id | ADR-0009 |
| Repeated/concurrent runs allowed; each request is its own run; no dedupe/serialization/ordering/idempotency promises; deterministic analytical output not guaranteed | ADR-0010 |
| Completed results are immutable, run-addressable research state; failed runs keep metadata only; results are not external links | ADR-0011 |

## Terms established

Analysis Scope, Owning Process, Analysis Request, Analysis Result, Artifact Identity, Artifact Version, UKG Version, Analysis Run, Analysis Core, Evaluation Harness, End User, Researcher, Evaluation Ground Truth, Input Failure, Completed Analysis, Execution Failure, Request-Level Fatal Failure, Input Diagnostic, Structural Traceability, Analysis Reproducibility, External Scenario–Test Link, Request/Correlation Identifier, provisional gap-situation names.

## Open / deferred (not decided)

- Result schema, status vocabulary, evidence model, explanation structure.
- Link-mutation authority (service REST call vs. subsystem after response).
- UKG storage technology, property graph vs. RDF, snapshot vs. delta, retention, caching.
- Physical analysis-result storage, retention/deletion, intermediate reasoning artifacts, caching.
- Whether artifact-specific KGs are independently versioned/persisted.
- BDD domain model, graph schemas, alignment strategy, query/reasoning mechanism (Cypher, LLM, GraphRAG).
- Scope identity derivation; multi-root scopes; reusable scenarios/tests; composite/application-level scope abstractions.
- Timeout value, cancellation, result envelope for execution failures.
- REST endpoint paths, payload schemas, error codes.
- Evaluation harness invocation (in-process/library vs service endpoint) — deferred to Evaluation/Prototype Architecture.
- Authentication/authorization — deferred.
- Ground-truth construction methodology.

## Working notes

- Commit `06dfdc3` contains the initial documentation baseline; `aefdede` finalized the Scope & System Boundary session. Later documentation changes are uncommitted.
- Domain Concepts & Ubiquitous Language Grill is also closed; see `docs/domain-concepts-summary.md` and ADR-0012–0015.
- Prototype Architectural Baseline Grill is closed; see `docs/prototype-architecture-baseline.md` and ADR-0016–0020. No code exists yet.
- `Dataset/` and research-library binaries are git-ignored; `resource-structure.txt` is intentionally untracked (UTF-16, stale).
