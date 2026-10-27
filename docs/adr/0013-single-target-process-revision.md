# ADR-0013: One target process revision per V0 scope

- **Status:** Accepted (narrows ADR-0007 for V0)
- **Date:** 2026-10-26
- **Scope:** Knowledge-Based Validation Service — V0 analysis scope

## Context

ADR-0007 generalized the analysis unit into an Analysis Scope that may include a root process, contained/called processes, scenarios, tests, and evidence. It did not say whether a scope may contain several representations or revisions of the same process.

Supporting multiple representations in one scope would require choosing between them, reconciling divergences, and defining which representation a finding refers to. Those are research questions of their own and are not needed to establish the validation approach.

## Decision

For V0, each Analysis Scope is centered on:

- **one Target Process**;
- **one declared authoritative revision** of that Process.

The analysis concerns that revision. Sub-Processes, Call Activities, and explicitly supplied called/supporting Processes remain allowed as supporting context, under the declared-membership rules (ADR-0007).

V0 does not:

- compare alternative BPMN representations of the target process inside one scope;
- compare multiple revisions of the target process inside one scope;
- resolve conflicts between competing representations.

Different revisions/representations belong to different scopes or artifact states, and therefore to different UKG versions.

## Consequences

- Findings refer to a single identifiable target process revision.
- Scope identity includes the authoritative target revision.
- Multi-representation comparison remains a possible later research direction, not a V0 capability.
- Supporting processes are context/dependencies, not additional analysis targets.

## Alternatives considered

- **Multiple revisions in one scope** — enables comparison, but requires divergence semantics and complicates provenance.
- **Multiple alternative representations** — raises reconciliation questions with no established method.
- **No declared target revision** — makes the analyzed artifact state ambiguous.
- **Forbid called/supporting processes** — contradicts BPMN behavior and ADR-0007.

## Open questions (not decided by this ADR)

- How the authoritative revision is identified and validated.
- Whether a later version supports multiple targets or revisions per scope.
- How supporting-process findings are attributed without being treated as additional targets.
