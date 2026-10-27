# ADR-0015: Verification vs. Validation in this thesis

- **Status:** Accepted
- **Date:** 2026-10-26
- **Scope:** Knowledge-Based Validation Service — research terminology

## Context

"Verification" and "validation" carry standard software-engineering meanings that do not match this thesis. Standard usage often treats verification as conformance of an implementation to a specification. In this thesis, the relevant distinction is different: whether the BPMN model is technically sound, versus whether available tests actually provide evidence for the expected behavior expressed by Scenarios.

This ambiguity matters because the service is named a validation service. Without an explicit definition, a reader could assume it checks BPMN correctness (deadlocks, control flow, exception handling) or that it validates stakeholder requirements directly.

## Decision

**Verification (thesis-specific):** whether the BPMN model itself is built correctly and is technically/structurally valid — e.g. deadlocks/control-flow defects, exception handling, required services/dependencies, structural soundness or executability. Conceptually: "Is the model built correctly?" It is not the responsibility of this service, and the thesis-specific meaning must not be confused with standard implementation-conformance usage.

**Validation:** whether modeled and tested behavior corresponds to the expected behavior expressed by the supplied behavioral Scenarios.

```text
Scenario              -> expected behavior
BPMN Process Model    -> representation of that behavior
Existing Test Case(s) -> potential evidence for validating that behavior
```

For each concrete Scenario, the service determines which existing Test Case or combination provides sufficient evidence to validate that expected behavior, given its representation in the target BPMN Process model.

The **origin of a Test Case is irrelevant**: manually authored, generated, or produced by another testing mechanism. The service evaluates the available test and evidence, not its provenance.

The service performs **evidence-based Validation Assessment**; it does not perform BPMN-model Verification.

**Validated** does not mean absolute stakeholder correctness. It means sufficient evidence was found relative to the supplied Scenario, the declared BPMN process/artifact state, the available Test Cases and evidence, and the declared Analysis Scope. The persisted status vocabulary remains deferred.

## Consequences

- Model-quality checks (deadlocks, control flow, exception handling, wiring) are explicitly outside the service.
- The thesis contribution is test-evidence validation against Scenarios, not code verification or model verification.
- Test generation provenance cannot be used to dismiss or privilege a Test Case.
- Findings are always qualified by the supplied Scenario, artifact state, scope, tests, and evidence.
- Documentation must not use "verification" in the standard conformance sense without qualification.

## Alternatives considered

- **Standard software-engineering V&V** (verification = implementation vs. specification; validation = stakeholder needs) — well known, but obscures the thesis focus on test evidence and BPMN representation.
- **Treat BPMN model checks as verification within the service** — expands scope into model analysis the thesis does not address.
- **Treat "validated" as absolute stakeholder correctness** — over-claims from limited, supplied evidence.
- **Use verification and validation interchangeably** — destroys the central research distinction.

## Open questions (not decided by this ADR)

- How "sufficient evidence" is determined.
- Persisted status vocabulary and how "Validated" is expressed there.
- Whether model-quality findings from external tools could later be incorporated as context.
