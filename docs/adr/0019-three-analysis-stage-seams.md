# ADR-0019: Three analysis stages as orchestration seams

- **Status:** Accepted
- **Date:** 2026-10-27
- **Scope:** Prototype analysis architecture

## Context

The research logic will grow from placeholders to candidate discovery, model-grounded structural traceability, and evidence-based validation assessment. If the first slice uses one monolithic engine, introducing those stages later would require rewriting orchestration and settled boundaries.

Algorithms, scoring, and evidence sufficiency are not yet designed and must not be guessed now.

## Decision

Establish three lightweight logical stages, called in order by the application orchestrator:

1. **Candidate Discovery**
2. **Structural Traceability**
3. **Validation Assessment**

These are extension points, not microservices and not algorithms. In the first slice they may be intentionally simple placeholders that return unresolved/insufficient outcomes.

The Target BPMN Process remains essential analytical context:

```text
Scenario -> represented modeled behavior -> relevant Test Case(s) -> validation evidence
```

Analysis must not collapse into context-free Scenario–Test linking.

## Consequences

- Orchestration shape is stable while stage implementations evolve.
- Placeholder behavior must be explicit, never disguised as real validation.
- Stage interfaces should stay narrow; passing entire infrastructure objects through them is prohibited.
- Premature scoring or evidence rules are avoided.

## Alternatives considered

- **Single AnalysisEngine** — fewer files now, but forces orchestration rewriting later.
- **Implementing real algorithms immediately** — outside the architectural slice and premature.
- **Microservices per stage** — operational overhead with no need.
- **Skipping traceability in V0** — contradicts the accepted model-grounded domain.

## Open questions

- Exact stage input/output types.
- Whether stages compose iteratively over candidates or per scenario.
- Where evidence sufficiency is decided.
- How stage outcomes are explained and persisted.
