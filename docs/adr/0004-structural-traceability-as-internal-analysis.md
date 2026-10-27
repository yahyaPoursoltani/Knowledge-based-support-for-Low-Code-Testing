# ADR-0004: Structural traceability is internal analysis, not a coverage deliverable

- **Status:** Accepted (gap taxonomy staged and renamed in ADR-0012; "semantic validation gap" is now "Semantic Validation Insufficiency", applicable only after representation and traceability)
- **Date:** 2026-10-26
- **Scope:** Knowledge-Based Validation Service (thesis implementation)

## Context

The thesis problem is that testing an implementation against a model does not establish that the model expresses stakeholder expectations. Distinguishing that from ordinary coverage requires distinguishing three ordered failure conditions:

1. behavior expressed by the supplied behavioral specification is not represented in the process model;
2. it is represented but lacks structural traceability to supplied tests;
3. it is represented and structurally traced, yet still lacks sufficient semantic validation evidence.

The third condition is the core of the research. Excluding coverage and traceability entirely would make situations 1–3 indistinguishable and would collapse the analysis back into conventional coverage thinking. Building a coverage management/reporting capability would instead make coverage the deliverable and shift effort away from semantic validation.

## Decision

Structural coverage and traceability are **in-scope as internal analysis**. The service may compute and expose them when needed for Scenario–Test assessment, gap classification, evidence analysis, or explanation.

They are **not** the primary deliverable. The service does not become a general-purpose test-coverage management or reporting subsystem.

The service may assess whether supplied BPMN behavior, scenarios, tests, and evidence are mutually supportive or inconsistent, but it must not claim absolute business correctness from the BPMN model alone, and it must not act as a substitute for stakeholder/domain-expert judgment when artifacts and evidence are insufficient.

The service must also not generate the empirical ground truth used to evaluate the thesis method.

## Consequences

- Coverage and traceability results must be reported together with the semantic-validation assessment, never as a standalone verdict.
- The three gap situations need distinguishable explanations in the Analysis Result.
- Evidence and analysis remain the focus; coverage computation is justified only by its role in assessment.
- The service may still lack evidence and must say so explicitly rather than infer absence of defects.
- Ground-truth construction stays outside the service, so evaluation design can remain independent of the method under test.

## Alternatives considered

- **Exclude coverage/traceability entirely** — keeps scope tight, but prevents distinguishing representation gaps from traceability gaps from semantic-validation gaps.
- **Build a coverage management/reporting subsystem** — familiar and easy to demonstrate, but makes coverage the deliverable and weakens the research contribution.
- **Treat structural coverage as proof of validation** — rejected; this is the conflation the research targets.

## Open questions (not decided by this ADR)

- How "a scenario is represented in the model" is determined.
- The semantics of the structural traceability relation.
- Final vocabulary for the gap situations and their statuses.
- Whether coverage/traceability information is persisted in the UKG or computed per analysis.
- How explanations distinguish the three situations without implying absolute correctness.
