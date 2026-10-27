# ADR-0012: Staged validation-failure taxonomy

- **Status:** Accepted
- **Date:** 2026-10-26
- **Scope:** Knowledge-Based Validation Service — domain semantics

## Context

Earlier documentation treated representation, traceability, and semantic validation as three distinct situations but did not order them. The researcher's refined taxonomy (`fig_Validation_Fail_Taxonomy.pdf`, not present in this repository at recording time; flow recorded from the researcher's statement) makes them staged conditions with stop branches.

An unordered, non-exclusive taxonomy would allow labeling one behavior with several failures simultaneously and would blur what MBTT means. It would also leave "semantic validation insufficiency" applicable to behavior that was never represented or traced.

## Decision

The V0 taxonomy is staged. Each branch stops at the first failing condition:

```text
Specified behavior
  -> Represented?                      No -> Representation Gap (stop)
  -> Structurally traced?              No -> Traceability Gap (stop)
  -> Sufficient semantic evidence?     No -> Semantic Validation Insufficiency (the MBTT condition) (stop)
  -> Validated (relative to available evidence)
```

- **Representation Gap** — behavior expressed by the supplied behavioral specification is not sufficiently represented in the supplied process model(s), relative to the specification and scope.
- **Traceability Gap** — represented behavior lacks the required structural trace to supplied tests; structural traceability is not semantic validation.
- **Semantic Validation Insufficiency** — represented **and** structurally traced, but evidence is insufficient to establish that the test validates the specified behavior. The earlier provisional name "semantic validation gap" is replaced; the meaning is not broadened.
- **MBTT** — the research interpretation corresponding exactly to the third failure stage. It is not the primary persisted status of an Analysis Result and not a label for missing tests or missing process behavior; the operational outcome is Semantic Validation Insufficiency, and an explanation may state that the condition corresponds to the Model-Bounded Testing Trap.
- **Validated** — sufficient evidence was found relative to the supplied Scenario, the declared BPMN process/artifact state, the available Test Cases and evidence, and the declared Analysis Scope. Not absolute stakeholder correctness (ADR-0015).

The stages are not simultaneous labels.

V0 does not introduce Contradictory Evidence or Validation Contradiction, a contradiction taxonomy, test-correctness adjudication, or artifact-repair logic. The service answers only whether the available tests and evidence suffice to validate the specified behavior; if not, the behavior is not established as validated. Evidence may weaken or contradict a claim in the general sense, but that is not a V0 gap or status classification.

## Consequences

- Findings name exactly one failure stage per behavior when a branch fails.
- MBTT remains a precise research condition and cannot be used for representation or traceability failures.
- Semantic Validation Insufficiency cannot be reported before representation and traceability are established.
- The service explains unsupported expected behavior without assigning fault to an artifact.
- Diagnostic ordering must be explicit in explanations and persisted results.

## Alternatives considered

- **Three independent, non-exclusive labels** — allows multiple simultaneous failures, but obscures which condition the analysis actually established and broadens insufficiency.
- **Broad semantic validation failure label** — collapses stages and loses the MBTT distinction.
- **Contradiction taxonomy** — would require adjudicating artifact correctness, which is out of V0 scope.
- **Treat MBTT as any missing-test condition** — conflates research condition with ordinary coverage gaps.

## Open questions (not decided by this ADR)

- Add `fig_Validation_Fail_Taxonomy.pdf` to the repository for source cross-checking.
- Evidence sufficiency criteria for the third stage.
- Exact explanation wording that may reference MBTT by name.
- How partial representation/trace coverage is recorded as analytical context.
- Exact explanation and result vocabulary.
