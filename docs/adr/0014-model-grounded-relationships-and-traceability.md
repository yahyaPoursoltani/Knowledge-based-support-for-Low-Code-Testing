# ADR-0014: Model-grounded analytical relationships and structural traceability

- **Status:** Accepted
- **Date:** 2026-10-26
- **Scope:** Knowledge-Based Validation Service — domain semantics

## Context

A Scenario–Test relationship can be expressed as a context-free link, but the thesis is about whether tests provide evidence for behavior represented in a process model. Treating relationships as context-free would allow textual similarity or an arbitrary association to stand in for traceability, and would detach MBTT from the modeled behavior that makes it meaningful.

At the same time, requiring complete step-by-step semantic validation before the traceability stage would turn structural traceability into heavy semantic reasoning and blur the distinction between stages 2 and 3.

## Decision

**Analytical Validation Relationship:** the analyzed Scenario–Test relationship within the context of the target Process model, Analysis Scope, and artifact state. It is not a context-free link; the analysis preserves:

```text
Scenario behavior -> representation in the BPMN Process model -> Test Case(s) -> available validation evidence
```

It may have a positive, insufficient, or otherwise unresolved analytical outcome.

**Structural traceability stage:** a Scenario passes when there is a defensible structural correspondence between:

- the behavior expressed by the Scenario;
- the representation of that behavior in the target BPMN Process model;
- at least one supplied Test Case.

Mere textual similarity, an arbitrary external link, or an unsupported Scenario–Test association does **not** establish structural traceability. Structural traceability is a model-grounded relation, **not semantic validation evidence by itself**.

The stage does not require complete step-by-step semantic validation of every Given/When/Then clause. Partial coverage of relevant modeled behavior is recorded as analytical context and may contribute to a later Semantic Validation Insufficiency; it is not automatically relabeled as a Traceability Gap.

Candidate Relationship (hypothesis) != Analytical Validation Relationship (analyzed, model-grounded) != External Scenario–Test Link (subsystem-persisted).

## Consequences

- Traceability judgments must be grounded in model correspondence, not just in links or text.
- MBTT remains tied to modeled behavior and cannot be inferred from context-free similarity.
- Partial coverage has a downstream effect rather than a premature gap label.
- Evidence from a test without a defensible model-grounded relation cannot reach the semantic-validation stage.
- The precise correspondence criteria and how partial coverage is recorded remain to be defined.

## Alternatives considered

- **Context-free Scenario–Test links** — simpler, but permits arbitrary associations and detaches validation from the model.
- **Full step-level coverage required before stage 3** — collapses traceability into semantic validation and adds heavy reasoning.
- **Any external link counts as structural trace** — lets unsupported associations pass the stage.
- **Treat partial coverage as a Traceability Gap** — mislabels behavior that is connected but not fully covered.

## Open questions (not decided by this ADR)

- What makes a structural correspondence "defensible".
- How partial coverage is represented as analytical context.
- Directionality and multiplicity of structural relations (one test to several scenarios and vice versa).
- Relationship between the Analytical Validation Relationship and the Claim/Assessment pair.
